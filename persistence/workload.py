import os
from migration.workload import Workload
from migration.json_decoder import get_workload
from .jsonpickler import JsonPickler

SCRIPT_PATH = os.path.dirname(__file__)
WORKLOADS_DIRNAME = os.path.join(SCRIPT_PATH, "workloads")


class WorkloadPickler(JsonPickler):
    def __init__(self, dirname=WORKLOADS_DIRNAME):
        super().__init__(dirname=dirname)

    def get_id(self, workload: Workload) -> str:
        return workload.ip

    def get_serializable(self, s: str) -> Workload:
        return get_workload(s)

    def is_possible_to_create(self, workload: Workload) -> (bool, str):
        for filename in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, filename), "r") as f:
                current = self.get_serializable(f.read())

                if current.ip == workload.ip:
                    return False, "Cannot create record with the same IP value"

        return True, ""

    def is_possible_to_update(self, old_workload: object, new_workload: object) -> (bool, str):
        if old_workload.ip == new_workload.ip:
            return False, "Cannot update IP value"

        return True, ""

    def fits(self, pickle_object: Workload, object: Workload) -> bool:
        if pickle_object is not None and object is not None:
            return pickle_object.ip == object.ip
        else:
            return pickle_object is None and object is None

        return True