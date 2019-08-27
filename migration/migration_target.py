from .credentials import Credentials
from .workload import Workload
from .serializable import Serializable

from enum import Enum


class CloudType(Enum):
    AWS = 1
    Azure = 2
    vSphere = 3
    vCloud = 4

    def repr_json(self):
        return dict(state=self.name)


class MigrationTarget(Serializable):
    def __init__(self, cloud_type: CloudType, cloud_credentials: Credentials, target_vm: Workload):
        self.cloud_type = cloud_type
        self.cloud_credentials = cloud_credentials
        self.target_vm = target_vm

    def repr_json(self):
        return dict(cloud_type=self.cloud_type, cloud_credentials=self.cloud_credentials, target_vm=self.target_vm)
