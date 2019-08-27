import unittest
import os

from migration.credentials import Credentials
from migration.migration_target import MigrationTarget, CloudType

from persistence.migration_target import MigrationTargetPickler

SCRIPT_PATH = os.path.dirname(__file__)
MIGRATION_TARGETS_DIRNAME = os.path.join(SCRIPT_PATH, "migration_targets")

migration_target_pickler = MigrationTargetPickler(dirname=MIGRATION_TARGETS_DIRNAME)


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        for filename in os.listdir(MIGRATION_TARGETS_DIRNAME):
            os.remove(os.path.join(MIGRATION_TARGETS_DIRNAME, filename))

    def test_create_and_read_one_record(self):
        credentials = Credentials("username", "password", None)
        migration_target = MigrationTarget(CloudType.Azure, credentials, None)
        migration_target_pickler.create(migration_target)

        ret = migration_target_pickler.read(migration_target)
        self.assertEqual(ret[0].cloud_type, CloudType.Azure.name)
        self.assertEqual(ret[0].cloud_credentials.username, "username")

    def test_create_and_read_several_records(self):
        credentials1 = Credentials("username", "password", "domain")
        migration_target1 = MigrationTarget(CloudType.Azure, credentials1, None)
        migration_target_pickler.create(migration_target1)

        credentials2 = Credentials("username", "password", None)
        migration_target2 = MigrationTarget(CloudType.Azure, credentials2, None)
        migration_target_pickler.create(migration_target2)

        ret = migration_target_pickler.read(migration_target2)
        self.assertEqual(len(ret), 2)

    def test_update(self):
        credentials = Credentials("username", "password", None)
        migration_target = MigrationTarget(CloudType.Azure, credentials, None)
        migration_target_pickler.create(migration_target)

        new_migration_target = MigrationTarget(CloudType.AWS, migration_target.cloud_credentials, None)
        migration_target_pickler.update(migration_target, new_migration_target)
        ret = migration_target_pickler.read(new_migration_target)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].cloud_type, CloudType.AWS.name)

    def test_delete(self):
        credentials = Credentials("user", "pass", None)
        migration_target = MigrationTarget(CloudType.Azure, credentials, None)
        migration_target_pickler.create(migration_target)
        migration_target_pickler.delete(migration_target)
        self.assertEqual(migration_target_pickler.read(migration_target), [])


if __name__ == '__main__':
    unittest.main()
