import os

from .jsonpickler import JsonPickler
from .credentials import CredentialsPickler
from .workload import WorkloadPickler

from migration.migration_target import MigrationTarget
from migration.json_decoder import get_migration_target

SCRIPT_PATH = os.path.dirname(__file__)
MIGRATION_TARGETS_DIRNAME = os.path.join(SCRIPT_PATH, "migration_targets")


class MigrationTargetPickler(JsonPickler):
    def __init__(self, dirname=MIGRATION_TARGETS_DIRNAME):
        super().__init__(dirname=dirname)
        self.credentials_pickler = CredentialsPickler()
        self.workload_pickler = WorkloadPickler()

    def get_id(self, migration_target: MigrationTarget) -> str:
        id_string = str(migration_target.cloud_type) + self.credentials_pickler.get_id(migration_target.cloud_credentials)

        if migration_target.target_vm is not None:
            id_string += self.workload_pickler.get_id(migration_target.target_vm)

        return id_string

    def get_serializable(self, s: str) -> MigrationTarget:
        return get_migration_target(s)

    def is_possible_to_update(self, old_obj: object, new_obj: object) -> (bool, str):
        return True, ""

    def is_possible_to_create(self, obj: object) -> (bool, str):
        return True, ""

    def fits(self, pickle_object: MigrationTarget, object: MigrationTarget) -> bool:
        if pickle_object is not None and object is not None:
            if object.cloud_credentials is not None:
                if not self.credentials_pickler.fits(pickle_object.cloud_credentials, object.cloud_credentials):
                    return False

            if object.target_vm is not None:
                if not self.workload_pickler.fits(pickle_object.target_vm, object.target_vm):
                    return False

            if object.cloud_type is not None:
                if pickle_object.cloud_type != object.cloud_type:
                    return False
        else:
            return pickle_object is None and object is None

        return True
