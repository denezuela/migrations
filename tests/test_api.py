import unittest
import requests
import json
import os
from time import sleep

from migration.workload import Workload
from migration.credentials import Credentials
from migration.mount_point import MountPoint
from migration.migration_target import MigrationTarget, CloudType
from migration.migration import Migration, MigrationState

from migration.json_encoder import ComplexEncoder

from persistence.migration import MigrationPickler

SCRIPT_PATH = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(SCRIPT_PATH)
DATA_PATH = os.path.join(PARENT_DIR, "persistence")
WORKLOADS_DIRNAME = os.path.join(DATA_PATH, "workloads")
MIGRATIONS_DIRNAME = os.path.join(DATA_PATH, "migrations")

migration_pickler = MigrationPickler()


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        if os.path.exists(MIGRATIONS_DIRNAME):
            for filename in os.listdir(MIGRATIONS_DIRNAME):
                os.remove(os.path.join(MIGRATIONS_DIRNAME, filename))

        if os.path.exists(WORKLOADS_DIRNAME):
            for filename in os.listdir(WORKLOADS_DIRNAME):
                os.remove(os.path.join(WORKLOADS_DIRNAME, filename))

    def test_hello(self):
        self.assertEqual(requests.get("http://127.0.0.1:5000/").text, "Hello World!")

    def test_workloads(self):
        credentials = Credentials("username", "password", "domain")
        workload = Workload("127.0.0.1", credentials, [MountPoint("C:\\", 1024)])
        data = json.dumps(workload, cls=ComplexEncoder)

        res = requests.post("http://127.0.0.1:5000/workloads/add", data=data)
        self.assertEqual(res.status_code, 200)
        response_json = json.loads(res.text)
        self.assertTrue(response_json["success"])

        new_workload = Workload("127.0.0.1", credentials, [MountPoint("E:\\", 1024)])
        new_workload_data = json.dumps(new_workload, cls=ComplexEncoder)
        new_data = json.dumps({'old': json.loads(data), 'new': json.loads(new_workload_data)})

        res = requests.post("http://127.0.0.1:5000/workloads/add", data=new_workload_data)
        self.assertEqual(res.status_code, 500)
        response_json = json.loads(res.text)
        self.assertFalse(response_json["success"])
        self.assertEqual(response_json['error'], "Cannot create record with the same IP value")

        res = requests.post("http://127.0.0.1:5000/workloads/update", data=new_data)
        self.assertEqual(res.status_code, 500)
        response_json = json.loads(res.text)
        self.assertFalse(response_json["success"])
        self.assertEqual(response_json['error'], "Cannot update IP value")

        res = requests.post("http://127.0.0.1:5000/workloads/delete", data=new_workload_data)
        self.assertEqual(res.status_code, 200)
        response_json = json.loads(res.text)
        self.assertTrue(response_json["success"])

    def test_run_migration(self):
        credentials = Credentials("username", "password", None)
        migration_target = MigrationTarget(CloudType.Azure, credentials, None)
        workload = Workload("127.0.0.1", credentials, [MountPoint("C:\\", 1024)])
        mount_points = [MountPoint("C:\\", 1024)]
        migration = Migration(mount_points, workload, migration_target)
        migration_pickler.create(migration)
        data = json.dumps(migration, cls=ComplexEncoder)

        res = requests.post("http://127.0.0.1:5000/migrations/run", data=data)
        self.assertEqual(res.status_code, 200)
        response_json = json.loads(res.text)
        self.assertTrue(response_json["success"])

    def test_migration_status(self):
        credentials = Credentials("username", "password", None)
        migration_target = MigrationTarget(CloudType.Azure, credentials, None)
        workload = Workload("127.0.0.1", credentials, [MountPoint("C:\\", 1024)])
        mount_points = [MountPoint("C:\\", 1024)]
        migration = Migration(mount_points, workload, migration_target)
        migration_pickler.create(migration)
        data = json.dumps(migration, cls=ComplexEncoder)

        res = requests.post("http://127.0.0.1:5000/migrations/run", data=data)
        self.assertEqual(res.status_code, 200)
        response_json = json.loads(res.text)
        self.assertTrue(response_json["success"])

        sleep(5)
        res = requests.post("http://127.0.0.1:5000/migrations/status", data=data)
        self.assertEqual(res.status_code, 200)
        response_json = json.loads(res.text)
        self.assertEqual(response_json["status"], MigrationState.RUNNING.name)


if __name__ == '__main__':
    unittest.main()
