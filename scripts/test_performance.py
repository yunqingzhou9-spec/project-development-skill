"""Offline behavior regressions for compact coordination and handoff safety."""
import hashlib
import json
import os
import socket
import sqlite3
import subprocess
import sys
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import coordinator
import handoff


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.outer = Path(self.temp.name).resolve()
        self.root = self.outer / 'repo'
        self.root.mkdir()
        self.git('init', '-q')
        (self.root / 'PROJECT_STATE.md').write_text('Current task: NONE\n')
        (self.root / 'file.txt').write_text('base\n')
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        self.registry = self.outer / 'private' / 'registry.sqlite3'
        self.store = coordinator.Coordinator(self.registry)
        self.addCleanup(self.store.close)
        self.store.operate('claim', 'fixture', 'fixture-repository', self.root, 'owner-one')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.DEVNULL)

    def op(self, command, **kwargs):
        return self.store.operate(command, 'fixture', 'fixture-repository', self.root, 'owner-one', 1, **kwargs)

    def helper(self, command, **kwargs):
        return handoff.run(command, 'fixture', 'fixture-repository', self.root, registry=self.registry, **kwargs)

    def prepare(self, **kwargs):
        return self.helper('prepare', owner='owner-one', generation=1, native_check_ref='fixture:native-workers-stopped', context={'active_task':'NONE','next_action':'Await instruction'}, **kwargs)

    def takeover(self, **kwargs):
        return self.helper('takeover', owner='owner-two', expected_generation=1, native_check_ref='fixture:native-old-owner-idle', **kwargs)

    def registry_fingerprint(self):
        return {str(p.relative_to(self.registry.parent)): (p.stat().st_mode, p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest()) for p in self.registry.parent.iterdir() if p.is_file()}

    def test_readonly_queries_do_not_change_database_or_mode(self):
        os.chmod(self.registry, 0o400)
        before = self.registry_fingerprint()
        with mock.patch.object(os, 'chmod', side_effect=AssertionError('chmod forbidden')):
            ro = coordinator.Coordinator(self.registry, read_only=True)
            try:
                self.assertEqual(ro.operate('status', 'fixture', 'fixture-repository', self.root, summary=True)['state'], 'ACTIVE')
                ro.operate('assert', 'fixture', 'fixture-repository', self.root, 'owner-one', 1)
                with self.assertRaises(coordinator.CoordinationError):
                    ro.operate('release', 'fixture', 'fixture-repository', self.root, 'owner-one', 1)
            finally:
                ro.close()
        self.assertEqual(before, self.registry_fingerprint())

    def test_missing_readonly_registry_is_not_created(self):
        target = self.outer / 'absent' / 'missing.sqlite3'
        with self.assertRaises((sqlite3.OperationalError, FileNotFoundError)):
            coordinator.Coordinator(target, read_only=True)
        self.assertFalse(target.parent.exists())

    def test_cli_status_uses_readonly_connection(self):
        before = self.registry_fingerprint()
        cli = [sys.executable, str(Path(coordinator.__file__)), 'status', '--registry',str(self.registry),'--project','fixture','--repository','fixture-repository','--checkout',str(self.root),'--summary']
        result = json.loads(subprocess.check_output(cli))
        self.assertNotIn('context', result)
        self.assertEqual(before,self.registry_fingerprint())

    def test_compact_output_has_unresolved_counts_without_history(self):
        self.op('begin',task='T1',work_key='review',attempt='a1',inputs='digest')
        self.op('resolve',attempt='a1',resolution_ref='fixture:stopped')
        self.op('begin',task='T2',work_key='review',attempt='a2',inputs='digest')
        result = self.op('status',summary=True)
        self.assertEqual(result['attempt_counts'],{'PREPARED':1,'RESOLVED':1})
        self.assertEqual([a['attempt'] for a in result['unresolved_attempts']],['a2'])
        self.assertNotIn('attempts',result)
        self.assertEqual(len(self.op('status')['attempts']),2)

    def test_dirty_roundtrip_preserves_bytes_and_increments_generation(self):
        (self.root/'file.txt').write_text('staged\n');self.git('add','file.txt')
        (self.root/'file.txt').write_text('unstaged\n')
        (self.root/'untracked.txt').write_text('private data\n')
        before=handoff.snapshot(self.root)
        released=self.prepare(); self.assertEqual(released['coordination']['state'],'RELEASED')
        self.assertIn(str(self.root),released['prompt'])
        claimed=self.takeover();self.assertEqual(claimed['coordination']['generation'],2)
        self.assertEqual(before,handoff.snapshot(self.root))
        with self.assertRaises(coordinator.CoordinationError): self.op('update',context={})

    def test_active_owner_and_unresolved_attempts_block(self):
        with self.assertRaises(coordinator.CoordinationError):self.takeover()
        self.op('begin',task='T',work_key='review',attempt='a',inputs='digest')
        with self.assertRaises(coordinator.CoordinationError):self.prepare()
        self.assertEqual(self.op('status')['state'],'ACTIVE')

    def test_requires_native_reconciliation_reference(self):
        with self.assertRaises(coordinator.CoordinationError):
            self.helper('prepare',owner='owner-one',generation=1,context={'active_task':'NONE','next_action':'wait'})
        self.prepare()
        with self.assertRaises(coordinator.CoordinationError):self.helper('takeover',owner='owner-two',expected_generation=1)

    def test_file_or_index_changes_block_takeover(self):
        (self.root/'untracked').write_text('before')
        self.prepare()
        (self.root/'untracked').write_text('after')
        with self.assertRaises(coordinator.CoordinationError):self.takeover()
        (self.root/'untracked').write_text('before')
        (self.root/'file.txt').write_text('new staged');self.git('add','file.txt');(self.root/'file.txt').write_text('base\n')
        with self.assertRaises(coordinator.CoordinationError):self.takeover()
        self.assertEqual(self.op('status')['state'],'RELEASED')

    def test_old_handoff_requires_manual_reconciliation(self):
        self.op('release')
        with self.assertRaisesRegex(coordinator.CoordinationError,'manual reconciliation'):self.takeover()

    def test_compare_and_claim_rejects_changed_generation(self):
        self.prepare()
        self.store.operate('claim','fixture','fixture-repository',self.root,'other')
        self.store.operate('release','fixture','fixture-repository',self.root,'other',2)
        with self.assertRaises(coordinator.CoordinationError):self.store.operate('claim','fixture','fixture-repository',self.root,'owner-two',expected_generation=1)

    def test_wrong_repository_and_stale_owner_rejected(self):
        with self.assertRaises(coordinator.CoordinationError):handoff.run('inspect','fixture','wrong',self.root,registry=self.registry)
        with self.assertRaises(coordinator.CoordinationError):self.helper('prepare',owner='old',generation=0,native_check_ref='fixture',context={'active_task':'NONE','next_action':'wait'})

    def test_state_path_escape_and_symlink_rejected(self):
        with self.assertRaises(coordinator.CoordinationError):self.prepare(state_path='../outside')
        (self.root/'link.md').symlink_to(self.root/'PROJECT_STATE.md')
        with self.assertRaises(coordinator.CoordinationError):self.prepare(state_path='link.md')

    def test_inspect_is_readonly_and_cannot_prove_native_state(self):
        before=self.registry_fingerprint()
        result=self.helper('inspect')
        self.assertEqual(result['native_writers'],'UNVERIFIED')
        self.assertEqual(before,self.registry_fingerprint())
        self.assertNotIn('context',result['coordination'])

    def test_no_network_commands_and_prepare_context_validation(self):
        original = subprocess.run
        def check(command, *args, **kwargs):
            self.assertNotIn('fetch',command);self.assertNotIn('ls-remote',command);self.assertNotIn('push',command)
            return original(command,*args,**kwargs)
        with mock.patch.object(subprocess,'run',side_effect=check):
            self.helper('inspect');self.prepare();self.takeover()

    def test_no_schema_repair_on_readonly_open(self):
        wrong=self.outer/'broken.sqlite3';db=sqlite3.connect(wrong);db.close();before=wrong.read_bytes()
        with self.assertRaises(sqlite3.Error):coordinator.Coordinator(wrong,read_only=True)
        self.assertEqual(before,wrong.read_bytes())

    def test_untracked_permissions_and_symlink_target_are_observed(self):
        file = self.root / 'private-script'
        file.write_text('content')
        before = handoff.snapshot(self.root)
        file.chmod(0o700)
        self.assertNotEqual(before, handoff.snapshot(self.root))
        link = self.root / 'untracked-link'
        link.symlink_to('one')
        before = handoff.snapshot(self.root)
        link.unlink(); link.symlink_to('two')
        self.assertNotEqual(before, handoff.snapshot(self.root))

    def test_release_context_validation_rolls_back_state(self):
        with self.assertRaises(coordinator.CoordinationError):
            self.op('release',context='invalid')
        self.assertEqual(self.op('status')['state'],'ACTIVE')

    def test_inspect_does_not_refresh_git_index(self):
        index = self.root / '.git' / 'index'
        before = (index.read_bytes(),index.stat().st_mtime_ns)
        self.helper('inspect')
        self.assertEqual(before,(index.read_bytes(),index.stat().st_mtime_ns))

    def test_wal_inspection_blocks_before_creating_sidecars(self):
        self.store.db.execute('PRAGMA journal_mode=WAL')
        self.store.close()
        self.assertFalse(Path(str(self.registry)+'-wal').exists())
        before=self.registry_fingerprint()
        with self.assertRaisesRegex(coordinator.CoordinationError,'WAL registry'):
            coordinator.Coordinator(self.registry,read_only=True)
        self.assertEqual(before,self.registry_fingerprint())

    def test_live_wal_is_not_ignored(self):
        self.store.db.execute('PRAGMA journal_mode=WAL')
        self.store.db.execute('UPDATE projects SET context=?',(json.dumps({'uncheckpointed':'must not ignore'}),))
        before=self.registry_fingerprint()
        with self.assertRaisesRegex(coordinator.CoordinationError,'WAL registry'):
            self.helper('inspect')
        self.assertEqual(before,self.registry_fingerprint())

    def test_dirty_crlf_normalization_change_blocks_takeover(self):
        (self.root/'.gitattributes').write_text('file.txt text\n')
        self.git('add','.gitattributes')
        self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','attributes')
        (self.root/'file.txt').write_bytes(b'dirty\r\n')
        before=handoff.snapshot(self.root)
        self.prepare()
        (self.root/'file.txt').write_bytes(b'dirty\n')
        self.assertNotEqual(before,handoff.snapshot(self.root))
        with self.assertRaises(coordinator.CoordinationError):self.takeover()
        self.assertEqual(self.op('status')['state'],'RELEASED')

    def test_malformed_saved_context_returns_structured_block(self):
        self.prepare()
        original=json.loads(self.store.db.execute('SELECT context FROM projects').fetchone()[0])
        for bad in ([],{'handoff':[]},{**original,'handoff':{**original['handoff'],'state_index':[]}}):
            self.store.db.execute('UPDATE projects SET context=?',(json.dumps(bad),))
            command=[sys.executable,str(Path(handoff.__file__)),'takeover','--registry',str(self.registry),'--project','fixture','--repository','fixture-repository','--checkout',str(self.root),'--owner','new','--expected-generation','1','--native-check-ref','fixture:idle']
            result=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(result.returncode,1)
            self.assertEqual(json.loads(result.stdout)['result'],'BLOCKED')
            self.assertNotIn('Traceback',result.stderr)
        self.assertEqual(self.op('status')['state'],'RELEASED')

    def test_cross_host_is_rejected_readonly(self):
        self.store.db.execute('UPDATE machine SET identity=?',('different-host',))
        with self.assertRaises(coordinator.CoordinationError):coordinator.Coordinator(self.registry,read_only=True)

    def test_single_call_verifies_release_claim_and_local_timing(self):
        self.op('update',context={'private_history':'not part of compact output'})
        released=self.prepare()
        self.assertEqual(released['verification']['status'],'VERIFIED')
        for value in ('owner-one','fixture-repository','generation 1',str(self.root),str(self.registry.resolve()),'--registry','PROJECT_STATE.md'):
            self.assertIn(value,released['prompt'])
        inspected=self.helper('inspect')
        self.assertEqual(inspected['saved_handoff'],{'generation':1,'state_path':'PROJECT_STATE.md'})
        self.assertNotIn('private_history',json.dumps(inspected))
        self.assertEqual(inspected['native_writers'],'UNVERIFIED')
        claimed=self.takeover()
        self.assertEqual(claimed['verification'],{'status':'VERIFIED','local_unchanged':True,'ownership_matches':True,'attempts_clear':True})
        self.assertEqual(claimed['coordination']['generation'],2)
        self.assertEqual(claimed['next_action'],'Await instruction')
        self.assertEqual(set(claimed['timing']['phases_ms']),{'registry_read','snapshot','validation','mutation','postcheck'})
        self.assertEqual(claimed['timing']['scope'],'helper_only')
        for key in ('end_to_end_ms','permission_wait_ms','model_ms','host_roundtrip_ms'):
            self.assertIsNone(claimed['timing'][key])
        self.assertAlmostEqual(sum(claimed['timing']['phases_ms'].values()),claimed['elapsed_ms'],delta=20)

    def test_elapsed_more_than_one_minute_never_aborts_claim(self):
        self.prepare()
        with mock.patch.object(handoff.time,'perf_counter',side_effect=range(0,1000,70)):
            claimed=self.takeover()
        self.assertGreater(claimed['elapsed_ms'],60000)
        self.assertEqual(claimed['verification']['status'],'VERIFIED')
        self.assertEqual(claimed['coordination']['generation'],2)

    def test_postclaim_change_reports_acquired_generation_without_rollback(self):
        self.prepare()
        original=handoff.snapshot
        calls=0
        def changed(checkout):
            nonlocal calls
            calls+=1
            if calls==2:
                (self.root/'file.txt').write_text('concurrent change')
            return original(checkout)
        with mock.patch.object(handoff,'snapshot',side_effect=changed):
            result=self.takeover()
        self.assertEqual(result['verification']['status'],'RECONCILE_REQUIRED')
        self.assertFalse(result['verification']['local_unchanged'])
        self.assertEqual(result['coordination']['generation'],2)
        self.assertEqual(self.op('status')['owner'],'owner-two')
        self.assertEqual(self.op('status')['state'],'ACTIVE')
        self.assertEqual((self.root/'file.txt').read_text(),'concurrent change')

    def test_postrelease_check_failure_withholds_prompt_and_preserves_release(self):
        original=handoff.snapshot
        calls=0
        def failed(checkout):
            nonlocal calls
            calls+=1
            if calls==3:
                raise OSError('fixture postcheck unavailable')
            return original(checkout)
        with mock.patch.object(handoff,'snapshot',side_effect=failed):
            result=self.prepare()
        self.assertEqual(result['verification']['status'],'RECONCILE_REQUIRED')
        self.assertNotIn('prompt',result)
        self.assertEqual(result['coordination']['state'],'RELEASED')
        self.assertEqual(self.op('status')['state'],'RELEASED')

    def test_postclaim_native_owner_change_is_not_reported_verified(self):
        self.prepare()
        original=handoff.observe
        calls=0
        def changed(*args,**kwargs):
            nonlocal calls
            calls+=1
            if calls==2:
                self.store.operate('release','fixture','fixture-repository',self.root,'owner-two',2)
            return original(*args,**kwargs)
        with mock.patch.object(handoff,'observe',side_effect=changed):
            result=self.takeover()
        self.assertEqual(result['verification']['status'],'RECONCILE_REQUIRED')
        self.assertFalse(result['verification']['ownership_matches'])

    def test_cli_record_is_private_and_does_not_change_checkout(self):
        self.prepare()
        before=handoff.snapshot(self.root)
        command=[sys.executable,str(Path(handoff.__file__)),'takeover','--registry',str(self.registry),'--project','fixture','--repository','fixture-repository','--checkout',str(self.root),'--owner','owner-two','--expected-generation','1','--native-check-ref','fixture:idle','--record']
        result=json.loads(subprocess.check_output(command))
        self.assertEqual(result['verification']['status'],'VERIFIED')
        path=Path(result['record']['path'])
        self.assertNotIn(self.root,path.parents)
        self.assertEqual(stat.S_IMODE(path.stat().st_mode),0o600)
        receipt=json.loads(path.read_text())
        self.assertEqual(receipt['coordination'],result['coordination'])
        self.assertEqual(receipt['timing'],result['timing'])
        self.assertNotIn('cli_elapsed_ms',receipt) # Written before the CLI finishes.
        self.assertGreaterEqual(result['cli_elapsed_ms'],result['elapsed_ms'])
        self.assertEqual(before,handoff.snapshot(self.root))

    def test_receipt_error_never_retries_or_rolls_back_success(self):
        self.prepare()
        args=['handoff.py','takeover','--registry',str(self.registry),'--project','fixture','--repository','fixture-repository','--checkout',str(self.root),'--owner','owner-two','--expected-generation','1','--native-check-ref','fixture:idle','--record']
        import io
        with mock.patch.object(sys,'argv',args), mock.patch.object(sys,'stdout',new_callable=io.StringIO) as output, mock.patch.object(handoff.os,'open',side_effect=PermissionError('fixture record denied')):
            self.assertEqual(handoff.main(),0)
        result=json.loads(output.getvalue())
        self.assertEqual(result['record']['status'],'UNAVAILABLE')
        self.assertEqual(result['verification']['status'],'VERIFIED')
        self.assertEqual(self.op('status')['generation'],2)

    def test_inspect_record_option_rejected_without_registry_writes(self):
        before=self.registry_fingerprint()
        command=[sys.executable,str(Path(handoff.__file__)),'inspect','--registry',str(self.registry),'--project','fixture','--repository','fixture-repository','--checkout',str(self.root),'--record']
        result=subprocess.run(command,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('inspect stays read-only',result.stderr)
        self.assertEqual(before,self.registry_fingerprint())

    def test_receipt_path_cannot_write_into_checkout(self):
        before=handoff.snapshot(self.root)
        result=handoff.record_result({},self.root/'registry.sqlite3',self.root,'takeover')
        self.assertEqual(result['status'],'UNAVAILABLE')
        self.assertEqual(before,handoff.snapshot(self.root))

    def test_prompt_registry_routes_takeover_when_default_differs(self):
        released=self.prepare()
        locator=json.loads(released['prompt'].split('(--registry) ',1)[1].split('；状态指针',1)[0])
        self.assertEqual(locator,str(self.registry.resolve()))
        absent=self.outer/'unrelated-default'/'registry.sqlite3'
        with mock.patch.object(handoff,'default_registry',return_value=absent):
            claimed=handoff.run('takeover','fixture','fixture-repository',self.root,registry=locator,
                                owner='owner-two',expected_generation=1,native_check_ref='fixture:fresh-idle')
        self.assertEqual(claimed['verification']['status'],'VERIFIED')
        self.assertEqual(claimed['coordination']['generation'],2)
        self.assertFalse(absent.parent.exists())


if __name__=='__main__':
    unittest.main()
