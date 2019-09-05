from .migration_target import MigrationTarget
from .mount_point import MountPoint
from .workload import Workload
from .serializable import Serializable

from enum import Enum
from time import sleep

X = 5


class MigrationState(Enum):
    NOT_STARTED = 1
    RUNNING = 2
    ERROR = 3
    SUCCESS = 4


class Migration(Serializable):
    def __init__(self, mount_points: [MountPoint], source: Workload, migration_target: MigrationTarget):
        self.mount_points = mount_points
        self.source = source
        self.migration_target = migration_target
        self.migration_state = MigrationState.NOT_STARTED

    def run(self):
        self.migration_state = MigrationState.RUNNING
        selected_mount_points_names = [str(mp.mount_point_name) for mp in self.mount_points]
        if "C:\\" not in selected_mount_points_names:
            raise Exception("Migration is now allowed when C:\\ is not selected")

        source_mount_point_names = [str(mp.mount_point_name) for mp in self.source.storage]
        storage = []
        for mount_point in self.mount_points:
            if mount_point.mount_point_name in source_mount_point_names:
                storage.append(mount_point)
        if len(storage) == 0:
            raise Exception("There are no selected mount points in source storage list")
        ip = self.source.ip
        credentials = self.source.credentials

        self.migration_target.target_vm = Workload(ip, credentials, storage)

        sleep(X * 60)
        self.migration_state = MigrationState.SUCCESS

    def repr_json(self):
        return dict(mount_points=self.mount_points, source=self.source, migration_target=self.migration_target,
                    migration_state=self.migration_state.name)
