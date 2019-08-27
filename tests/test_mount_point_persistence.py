import unittest
import os

from persistence.mount_point import MountPointPickler

from migration.mount_point import MountPoint

SCRIPT_PATH = os.path.dirname(__file__)
MOUNT_POINTS_DIRNAME = os.path.join(SCRIPT_PATH, "mount_points")

mount_point_pickler = MountPointPickler(dirname=MOUNT_POINTS_DIRNAME)


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        for filename in os.listdir(MOUNT_POINTS_DIRNAME):
            os.remove(os.path.join(MOUNT_POINTS_DIRNAME, filename))

    def test_create_and_read_one_record(self):
        mount_point = MountPoint("C:\\", 1024)
        mount_point_pickler.create(mount_point)
        ret = mount_point_pickler.read(mount_point)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].mount_point_name, "C:\\")
        self.assertEqual(ret[0].size, 1024)

    def test_create_and_read_several_records(self):
        mount_point1 = MountPoint("C:\\", 1024)
        mount_point_pickler.create(mount_point1)

        mount_point2 = MountPoint("C:\\", None)
        mount_point_pickler.create(mount_point2)

        ret = mount_point_pickler.read(mount_point2)
        self.assertEqual(len(ret), 2)

    def test_update(self):
        mount_point = MountPoint("E:\\", 4096)
        mount_point_pickler.create(mount_point)
        new_mount_point = MountPoint("E:\\", 2048)
        mount_point_pickler.update(mount_point, new_mount_point)
        ret = mount_point_pickler.read(new_mount_point)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].size, 2048)

    def test_delete(self):
        mount_point = MountPoint("C:\\", 4096)
        mount_point_pickler.create(mount_point)
        mount_point_pickler.delete(mount_point)
        self.assertEqual(mount_point_pickler.read(mount_point), [])


if __name__ == '__main__':
    unittest.main()

