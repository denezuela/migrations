import unittest
import os

from migration.workload import Workload
from migration.credentials import Credentials
from migration.mount_point import MountPoint

from persistence.workload import WorkloadPickler

SCRIPT_PATH = os.path.dirname(__file__)
WORKLOADS_DIRNAME = os.path.join(SCRIPT_PATH, "workloads")

workload_pickler = WorkloadPickler(dirname=WORKLOADS_DIRNAME)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        for filename in os.listdir(WORKLOADS_DIRNAME):
            os.remove(os.path.join(WORKLOADS_DIRNAME, filename))

    def test_create_and_read_one_record(self):
        credentials = Credentials("username", "password", "domain")
        workload = Workload("192.168.0.1", credentials, [MountPoint("C:\\", 1024)])
        workload_pickler.create(workload)
        ret = workload_pickler.read(workload)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].ip, "192.168.0.1")
        self.assertEqual(ret[0].credentials.username, "username")
        self.assertEqual(ret[0].storage[0].mount_point_name, "C:\\")

    def test_update(self):
        credentials = Credentials("user", "qwerty", None)
        workload = Workload("8.8.8.8", credentials, [MountPoint("C:\\", 1024)])
        workload_pickler.create(workload)

        credentials = Credentials("new_user", "qwerty", None)
        new_workload = Workload("7.7.7.7", credentials, [MountPoint("C:\\", 1024)])
        workload_pickler.update(workload, new_workload)

        ret = workload_pickler.read(new_workload)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].ip, "7.7.7.7")
        self.assertEqual(ret[0].credentials.username, "new_user")
        self.assertEqual(ret[0].storage[0].mount_point_name, "C:\\")

    def test_create_with_the_same_ip(self):
        credentials = Credentials("username", "password", "domain")
        workload = Workload("1.1.1.1", credentials, [MountPoint("C:\\", 1024)])

        workload_pickler.create(workload)
        with self.assertRaises(Exception):
            workload = Workload("1.1.1.1", credentials, [MountPoint("E:\\", 1024)])
            workload_pickler.create(workload)

    def test_update_with_the_same_ip(self):
        credentials = Credentials("username", "password", "domain")
        workload = Workload("4.4.4.4", credentials, [MountPoint("C:\\", 1024)])

        workload_pickler.create(workload)
        with self.assertRaises(Exception):
            new_workload = Workload("4.4.4.4", credentials, [MountPoint("E:\\", 1024)])
            workload_pickler.update(workload, new_workload)

    def test_delete(self):
        credentials = Credentials("temp_user", "password", "domain")
        workload = Workload("3.3.3.3", credentials, [MountPoint("C:\\", 1024)])
        workload_pickler.create(workload)
        workload_pickler.delete(workload)
        self.assertEqual(workload_pickler.read(workload), [])


if __name__ == '__main__':
    unittest.main()
