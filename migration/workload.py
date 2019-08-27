from .credentials import Credentials
from .mount_point import MountPoint


class Workload:
    def __init__(self, ip: str, credentials: Credentials, storage: [MountPoint]):
        if ip is not None:
            self._ip = ip
        else:
            raise TypeError("IP should not be None")

        self.credentials = credentials
        self.storage = storage

    @property
    def ip(self):
        return self._ip

    def repr_json(self):
        return dict(ip=self.ip, credentials=self.credentials, storage=self.storage)
