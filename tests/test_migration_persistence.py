import unittest
import os

from persistence.migration import MigrationPickler

from migration.workload import Workload
from migration.migration_target import MigrationTarget, CloudType
from migration.credentials import Credentials
from migration.migration import Migration
from migration.mount_point import MountPoint

SCRIPT_PATH = os.path.dirname(__file__)
MIGRATIONS_DIRNAME = os.path.join(SCRIPT_PATH, "migrations")

migration_pickler = MigrationPickler(dirname=MIGRATIONS_DIRNAME)


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        for filename in os.listdir(MIGRATIONS_DIRNAME):
            os.remove(os.path.join(MIGRATIONS_DIRNAME, filename))

    def test_create_and_read(self):
        credentials = Credentials("username", "password", None)
        migration_target = MigrationTarget(CloudType.Azure, credentials, None)
        workload = Workload("127.0.0.1", credentials, [])
        mount_points = [MountPoint("C:\\", 1024)]
        migration = Migration(mount_points, workload, migration_target)
        migration_pickler.create(migration)

        ret = migration_pickler.read(migration)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].migration_target.cloud_type, CloudType.Azure)
        self.assertEqual(ret[0].source.credentials.username, "username")

    def test_create_and_read_several_records(self):
        credentials1 = Credentials("username", "password", None)
        migration_target1 = MigrationTarget(CloudType.Azure, credentials1, Workload("127.0.0.1", credentials1, []))
        workload1 = Workload("127.0.0.1", credentials1, [])
        mount_points1 = [MountPoint("C:\\", 1024)]
        migration1 = Migration(mount_points1, workload1, migration_target1)
        migration_pickler.create(migration1)

        credentials2 = Credentials("username", "password", None)
        migration_target2 = MigrationTarget(CloudType.Azure, credentials2, None)
        workload2 = Workload("127.0.0.1", credentials2, [])
        mount_points2 = [MountPoint("C:\\", 1024)]
        migration2 = Migration(mount_points2, workload2, migration_target2)
        migration_pickler.create(migration2)

        ret = migration_pickler.read(migration2)
        self.assertEqual(len(ret), 2)

    def test_update(self):
        credentials = Credentials("new_user", "password", None)
        migration_target = MigrationTarget(CloudType.Azure, credentials, None)
        workload = Workload("127.0.0.1", credentials, [])
        mount_points = [MountPoint("C:\\", 1024)]
        migration = Migration(mount_points, workload, migration_target)
        migration_pickler.create(migration)

        mount_points = [MountPoint("E:\\", 1024)]
        new_migration = Migration(mount_points, workload, migration_target)
        migration_pickler.update(migration, new_migration)
        ret = migration_pickler.read(new_migration)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].mount_points[0].mount_point_name, "E:\\")

    def test_delete(self):
        credentials = Credentials("username", "new_password", None)
        migration_target = MigrationTarget(CloudType.AWS, credentials, Workload("127.0.0.1", credentials, []))
        workload = Workload("127.0.0.1", credentials, [])
        mount_points = [MountPoint("C:\\", 1024)]
        migration = Migration(mount_points, workload, migration_target)
        migration_pickler.create(migration)
        migration_pickler.delete(migration)
        self.assertEqual(migration_pickler.read(migration_target), [])


if __name__ == '__main__':
    unittest.main()