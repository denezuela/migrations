import unittest
import requests
import json
import os

from migration.workload import Workload
from migration.credentials import Credentials
from migration.mount_point import MountPoint

from migration.json_encoder import ComplexEncoder

SCRIPT_PATH = os.path.dirname(__file__)
print(SCRIPT_PATH)
PARENT_DIR = os.path.dirname(SCRIPT_PATH)
print(PARENT_DIR)
DATA_PATH = os.path.join(PARENT_DIR, "persistence")
WORKLOADS_DIRNAME = os.path.join(DATA_PATH, "workloads")
MIGRATIONS_DIRNAME = os.path.join(DATA_PATH, "migrations")


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

    def test_add_workload(self):
        credentials = Credentials("username", "password", "domain")
        workload = Workload("127.0.0.1", credentials, [MountPoint("C:\\", 1024)])
        data = json.dumps(workload, cls=ComplexEncoder)
        res = requests.post("http://127.0.0.1:5000/workloads/add", data=data)
        self.assertEqual(res.status_code, 200)
        response_json = json.loads(res.text)
        self.assertTrue(response_json["success"])


if __name__ == '__main__':
    unittest.main()
