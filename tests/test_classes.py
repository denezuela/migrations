import unittest
import json

from migration.workload import Workload
from migration.mount_point import MountPoint
from migration.migration import Migration, MigrationState
from migration.credentials import Credentials
from migration.migration_target import MigrationTarget, CloudType
from migration.json_encoder import ComplexEncoder

class MyTestCase(unittest.TestCase):
    def test_normal_migration(self):
        selected = [MountPoint("C:\\", 1024), MountPoint("E:\\", 2048)]

        source_credentials = Credentials("username", "password", "domain")
        storage = [MountPoint("C:\\", 1024), MountPoint("E:\\", 2048), MountPoint("D:\\", 2048)]
        source = Workload("127.0.0.1", source_credentials, storage)

        cloud_credentials = Credentials("username", "password", "cloud")
        target = MigrationTarget(CloudType.vSphere, cloud_credentials, None)

        migration = Migration(selected, source, target)
        migration.run()
        self.assertEqual(migration.migration_target.target_vm.ip, "127.0.0.1")
        self.assertEqual(migration.migration_target.target_vm.credentials.username, "username")
        self.assertEqual(migration.migration_target.target_vm.credentials.password, "password")
        self.assertEqual(migration.migration_target.target_vm.credentials.domain, "domain")
        self.assertEqual([(s.mount_point_name, s.size) for s in migration.migration_target.target_vm.storage],
                         [('C:\\', 1024), ('E:\\', 2048)])
        self.assertEqual(migration.migration_state, MigrationState.SUCCESS)

    def test_c_not_allowed(self):
        selected = [MountPoint("E:\\", 2048)]

        source_credentials = Credentials("username", "password", "domain")
        storage = [MountPoint("C:\\", 1024), MountPoint("E:\\", 2048), MountPoint("D:\\", 2048)]
        source = Workload("localhost", source_credentials, storage)

        cloud_credentials = Credentials("username", "password", "cloud")
        target = MigrationTarget(CloudType.vSphere, cloud_credentials, None)

        with self.assertRaises(Exception):
            migration = Migration(selected, source, target)
            migration.run()

    def test_no_selected_storages_in_source(self):
        selected = [MountPoint("C:\\", 1024), MountPoint("E:\\", 2048)]

        source_credentials = Credentials("username", "password", "domain")
        storage = [MountPoint("D:\\", 2048), MountPoint("F:\\", 2048)]
        source = Workload("localhost", source_credentials, storage)

        cloud_credentials = Credentials("username", "password", "cloud")
        target = MigrationTarget(CloudType.vSphere, cloud_credentials, None)

        with self.assertRaises(Exception):
            migration = Migration(selected, source, target)
            migration.run()

    def test_json_repr(self):
        credentials = Credentials("username", "password", None)
        self.assertEqual(json.dumps(credentials.repr_json(), cls=ComplexEncoder),
                         '{"username": "username", "password": "password", "domain": null}')

        mount_point = MountPoint('C:\\', 1024)
        self.assertEqual(json.dumps(mount_point.repr_json(), cls=ComplexEncoder),
                         r'{"mount_point_name": "C:\\", "size": 1024}')

        workload = Workload("127.0.0.1", credentials, [mount_point])
        self.assertEqual(json.dumps(workload.repr_json(), cls=ComplexEncoder),
                         '{"ip": "127.0.0.1", '
                         '"credentials": {"username": "username", "password": "password", "domain": null}, '
                         r'"storage": [{"mount_point_name": "C:\\", "size": 1024}]}')

        migration_target = MigrationTarget(CloudType.AWS, credentials, workload)
        self.assertEqual(json.dumps(migration_target.repr_json(), cls=ComplexEncoder),
                         '{"cloud_type": {"state": "AWS"}, '
                         '"cloud_credentials": {"username": "username", "password": "password", "domain": null}, '
                         '"target_vm": {"ip": "127.0.0.1", "credentials":'
                         ' {"username": "username", "password": "password", "domain": null}, '
                         r'"storage": [{"mount_point_name": "C:\\", "size": 1024}]}}')

        migration = Migration([mount_point], workload, migration_target)
        self.assertEqual(json.dumps(migration.repr_json(), cls=ComplexEncoder),
                         r'{"mount_points": [{"mount_point_name": "C:\\", "size": 1024}], '
                         '"source": {"ip": "127.0.0.1", '
                         '"credentials": {"username": "username", "password": "password", "domain": null}, '
                         r'"storage": [{"mount_point_name": "C:\\", "size": 1024}]}, '
                         '"migration_target": {"cloud_type": {"state": "AWS"}, '
                         '"cloud_credentials": {"username": "username", "password": "password", "domain": null}, '
                         '"target_vm": {"ip": "127.0.0.1", '
                         '"credentials": {"username": "username", "password": "password", "domain": null}, '
                         r'"storage": [{"mount_point_name": "C:\\", "size": 1024}]}}, '
                         '"migration_state": {"state": "NOT_STARTED"}}')


if __name__ == '__main__':
    unittest.main()
