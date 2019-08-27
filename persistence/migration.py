import os

from .jsonpickler import JsonPickler
from .migration_target import MigrationTargetPickler
from .workload import WorkloadPickler
from .mount_point import MountPointPickler

from migration.migration import Migration
from migration.json_decoder import get_migration

SCRIPT_PATH = os.path.dirname(__file__)
MIGRATIONS_DIRNAME = os.path.join(SCRIPT_PATH, "migrations")


class MigrationPickler(JsonPickler):
    def __init__(self, dirname=MIGRATIONS_DIRNAME):
        super().__init__(dirname=dirname)
        self.migration_target_pickler = MigrationTargetPickler()
        self.workload_pickler = WorkloadPickler()
        self.mount_point_pickler = MountPointPickler()

    def get_id(self, migration: Migration) -> str:
        id_string = self.migration_target_pickler.get_id(migration.migration_target)
        id_string += self.workload_pickler.get_id(migration.source)
        for point in migration.mount_points:
            id_string += self.mount_point_pickler.get_id(point)

        return id_string

    def get_serializable(self, s: str) -> Migration:
        return get_migration(s)

    def is_possible_to_update(self, old_obj: object, new_obj: object) -> (bool, str):
        return True, ""

    def is_possible_to_create(self, obj: object) -> (bool, str):
        return True, ""

    def fits(self, pickle_object: Migration, object: Migration) -> bool:
        if pickle_object is not None and object is not None:

            if object.source is not None:
                if not self.workload_pickler.fits(pickle_object.source, object.source):
                    return False

            if object.migration_target is not None:
                if not self.migration_target_pickler.fits(pickle_object.migration_target, object.migration_target):
                    return False

            if object.mount_points is not None:
                if len(pickle_object.mount_points) != len(object.mount_points):
                    return False
                for index, point in enumerate(pickle_object.mount_points):
                    if not self.mount_point_pickler.fits(point, object.mount_points[index]):
                        return False
        else:
            return pickle_object is None and object is None

        return True
