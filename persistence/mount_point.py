import os

from .jsonpickler import JsonPickler
from migration.json_decoder import get_mount_point

from migration.mount_point import MountPoint

SCRIPT_PATH = os.path.dirname(__file__)
MOUNT_POINTS_DIRNAME = os.path.join(SCRIPT_PATH, "mount_points")


class MountPointPickler(JsonPickler):
    def __init__(self, dirname=MOUNT_POINTS_DIRNAME):
        super().__init__(dirname=dirname)

    def get_id(self, mount_point: MountPoint) -> str:
        return mount_point.mount_point_name + str(mount_point.size)

    def get_serializable(self, s: str) -> MountPoint:
        return get_mount_point(s)

    def is_possible_to_update(self, old_obj: object, new_obj: object) -> (bool, str):
        return True, ""

    def is_possible_to_create(self, obj: object) -> (bool, str):
        return True, ""

    def fits(self, pickle_object: MountPoint, object: MountPoint) -> bool:
        if pickle_object is not None and object is not None:
            if pickle_object.mount_point_name is not None:
                if pickle_object.mount_point_name != object.mount_point_name:
                    return False

            if object.size is not None:
                if pickle_object.size != object.size:
                    return False
        else:
            return pickle_object is None and object is None

        return True