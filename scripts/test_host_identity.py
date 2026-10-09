"""Stable identity and explicit legacy reconciliation regression tests."""
import hashlib
import json
import plistlib
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import coordinator as c

class HostTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.outer = Path(self.temp.name).resolve()
        self.root = self.outer / 'repo'; self.root.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.path = self.outer / 'registry.sqlite3'
        self.identity = mock.patch.object(c, 'machine_identity', return_value='machine-a')
        self.identity.start(); self.addCleanup(self.identity.stop)
        self.store = c.Coordinator(self.path); self.addCleanup(self.store.close)
        self.store.operate('claim', 'project', 'repo', self.root, 'owner')
        self.evidence = self.outer/'evidence.json'
        self.evidence.write_text(json.dumps(dict(authorization_ref='human:approved',
            native_check_ref='native:all-complete', same_machine_basis='explicit local continuity')))
        self.backup = self.outer/'backup.sqlite3'

    def legacy(self):
        self.store.db.execute('DROP TABLE machine')
        self.store.db.execute('DROP TABLE host_projects')
        self.store.db.execute('DROP TABLE host_migrations')
        self.store.db.execute("UPDATE host SET name='old-host'")

    def migrate(self, **kw):
        args=dict(registry=self.path, project='project', repository='repo', checkout=self.root,
                  owner='owner', generation=1, expected_host='old-host', backup=self.backup,
                  evidence_ref=self.evidence, confirm_same_machine=True)
        args.update(kw)
        return c.migrate_host(**args)

    def rows(self):
        return {t:[tuple(r) for r in self.store.db.execute('SELECT * FROM '+t)]
                for t in ('host','projects','roots','attempts')}

    def test_hostname_change_accepts_read_write(self):
        with mock.patch.object(c.socket, 'gethostname', return_value='renamed'):
            for readonly in (True, False):
                store=c.Coordinator(self.path, read_only=readonly)
                self.assertEqual(store.operate('assert','project','repo',self.root,'owner',1)['generation'],1)
                store.close()

    def test_different_machine_refuses_without_changes(self):
        before=self.path.read_bytes()
        with mock.patch.object(c,'machine_identity',return_value='machine-b'):
            for ro in (True, False):
                with self.assertRaises(c.CoordinationError):c.Coordinator(self.path,read_only=ro)
        self.assertEqual(before,self.path.read_bytes())

    def test_unavailable_identity_never_falls_back(self):
        before=self.path.read_bytes()
        with mock.patch.object(c,'machine_identity',side_effect=c.CoordinationError('unavailable')):
            with self.assertRaises(c.CoordinationError):c.Coordinator(self.path)
        self.assertEqual(before,self.path.read_bytes())

    def test_legacy_normal_operations_never_migrate(self):
        self.legacy(); before=self.path.read_bytes()
        for ro in (True,False):
            with self.assertRaisesRegex(c.CoordinationError,'explicit migrate-host'):
                c.Coordinator(self.path,read_only=ro)
        self.assertEqual(before,self.path.read_bytes());self.assertFalse(self.backup.exists())

    def test_migration_preserves_history_and_exact_backup(self):
        self.store.operate('begin','project','repo',self.root,'owner',1,
                           task='T',work_key='review',attempt='a',inputs='digest')
        self.store.operate('resolve','project','repo',self.root,'owner',1,
                           attempt='a',resolution_ref='native:stopped')
        self.store.operate('update','project','repo',self.root,'owner',1,context={'keep':'history'})
        self.legacy();before=self.path.read_bytes();rows=self.rows()
        with mock.patch.object(c.socket,'gethostname',return_value='renamed'):
            result=self.migrate()
        self.assertEqual(result['generation'],1)
        self.assertEqual(before,self.backup.read_bytes());self.assertEqual(rows,self.rows())
        self.assertEqual(self.backup.stat().st_mode & 0o777,0o600)
        audit=json.loads(self.store.db.execute('SELECT audit FROM host_migrations').fetchone()[0])
        self.assertEqual(audit['backup_sha256'],hashlib.sha256(before).hexdigest())
        self.assertEqual(audit['evidence_sha256'],hashlib.sha256(self.evidence.read_bytes()).hexdigest())
        store=c.Coordinator(self.path,read_only=True);store.close()
        with self.assertRaisesRegex(c.CoordinationError,'Already bound'):
            self.migrate(backup=self.outer/'second.sqlite3')
        self.assertFalse((self.outer/'second.sqlite3').exists())

    def test_migration_expectation_mismatches_are_nonmutating(self):
        self.legacy();before=self.path.read_bytes()
        for delta in ({'confirm_same_machine':False},{'owner':'other'},{'generation':2},
                      {'expected_host':'other'},{'repository':'other'}, {'project':'other'},
                      {'backup':self.root/'private.sqlite3'}):
            with self.subTest(delta=delta),self.assertRaises(c.CoordinationError):self.migrate(**delta)
            self.assertEqual(before,self.path.read_bytes());self.assertFalse(self.backup.exists())

    def test_unbound_common_directory_blocked(self):
        self.legacy();other=self.outer/'other';other.mkdir()
        subprocess.run(['git','init','-q',str(other)],check=True)
        with self.assertRaisesRegex(c.CoordinationError,'common-directory'):self.migrate(checkout=other)

    def test_unresolved_target_blocks_but_other_projects_are_preserved(self):
        self.store.operate('begin','project','repo',self.root,'owner',1,
                           task='T',work_key='review',attempt='a',inputs='digest')
        self.legacy()
        with self.assertRaisesRegex(c.CoordinationError,'attempts'):self.migrate()
        self.store.db.execute("UPDATE attempts SET state='RESOLVED'")
        self.store.db.execute("INSERT INTO projects VALUES ('other','other','owner',1,'RELEASED','{}')")
        self.store.db.execute("INSERT INTO attempts VALUES ('other','other-a','T','work','digest',1,'DISPATCHED','native',NULL,NULL,NULL)")
        before=self.rows()
        self.migrate()
        self.assertEqual(before,self.rows())
        store=c.Coordinator(self.path)
        try:
            with self.assertRaisesRegex(c.CoordinationError,'another project'):
                store.operate('status','other','other',self.root)
            self.assertEqual(store.operate('assert','project','repo',self.root,'owner',1)['generation'],1)
        finally:store.close()

    def test_backup_and_evidence_cannot_be_overwritten_or_omitted(self):
        self.legacy();self.backup.write_bytes(b'keep')
        with self.assertRaises(c.CoordinationError):self.migrate()
        self.assertEqual(self.backup.read_bytes(),b'keep')
        self.evidence.write_text('{}')
        with self.assertRaises(c.CoordinationError):self.migrate(backup=self.outer/'new.sqlite3')

    def test_wal_migration_refuses_without_backup(self):
        self.legacy();self.store.db.execute('PRAGMA journal_mode=WAL')
        with self.assertRaisesRegex(c.CoordinationError,'WAL'):self.migrate()
        self.assertFalse(self.backup.exists())

    def test_failed_audit_write_rolls_back_but_retains_backup(self):
        self.legacy();self.store.db.execute('CREATE TABLE host_migrations (audit TEXT)')
        before=self.path.read_bytes();rows=self.rows()
        with self.assertRaises(sqlite3.Error):self.migrate()
        self.assertEqual(before,self.backup.read_bytes());self.assertEqual(rows,self.rows())
        self.assertIsNone(self.store.db.execute("SELECT 1 FROM sqlite_master WHERE name='machine'").fetchone())

class ProviderTests(unittest.TestCase):
    def test_darwin_identity_hashes_raw_value_and_ignores_hostname(self):
        raw='12345678-1234-1234-1234-123456789abc'
        result=subprocess.CompletedProcess([],0,plistlib.dumps([{'IOPlatformUUID':raw}]))
        with mock.patch.object(c.platform,'system',return_value='Darwin'),mock.patch.object(c.subprocess,'run',return_value=result):
            one=c.machine_identity()
            with mock.patch.object(c.socket,'gethostname',return_value='changed'):
                self.assertEqual(one,c.machine_identity())
        self.assertEqual(len(one),64);self.assertNotIn(raw,one)

    def test_provider_invalid_or_denied_blocks(self):
        for value in ('', 'invalid', '0'*32):
            with mock.patch.object(c.platform,'system',return_value='Linux'),mock.patch.object(Path,'read_text',return_value=value):
                with self.assertRaisesRegex(c.CoordinationError,'no hostname fallback'):c.machine_identity()
        with mock.patch.object(c.platform,'system',return_value='Darwin'),mock.patch.object(c.subprocess,'run',side_effect=PermissionError('denied')):
            with self.assertRaises(c.CoordinationError):c.machine_identity()

if __name__=='__main__':unittest.main()
