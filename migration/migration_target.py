from .credentials import Credentials
from .workload import Workload

from enum import Enum


class CloudType(Enum):
    AWS = 1
    Azure = 2
    vSphere = 3
    vCloud = 4


class MigrationTarget:
    def __init__(self, cloud_type: CloudType, cloud_credentials: Credentials, target_vm: Workload):
        self.cloud_type = cloud_type
        self.cloud_credentials = cloud_credentials
        self.target_vm = target_vm
