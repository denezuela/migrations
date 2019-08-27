import json

from .credentials import Credentials
from .mount_point import MountPoint
from .workload import Workload
from .migration_target import MigrationTarget, CloudType
from .migration import Migration, MigrationState


def get_credentials(s: str) -> Credentials:
    if s == "null":
        return None

    json_ = json.loads(s)
    return Credentials(json_['username'], json_['password'], json_['domain'])


def get_mount_point(s: str) -> MountPoint:
    if s == "null":
        return None

    json_ = json.loads(s)
    return MountPoint(json_['mount_point_name'].replace("\\\\", "\\"), json_['size'])


def get_workload(s: str) -> Workload:
    if s == "null":
        return None

    json_ = json.loads(s)
    ip = json_['ip']
    credentials = get_credentials(json.dumps(json_['credentials']))
    storage = [get_mount_point(json.dumps(s)) for s in json_['storage']]
    return Workload(ip, credentials, storage)


def get_cloud_type(s: str) -> CloudType:
    if s == "null":
        return None
    if s == "AWS":
        return CloudType.AWS
    if s == "Azure":
        return CloudType.Azure
    if s == "vSphere":
        return CloudType.vSphere
    if s == "vCloud":
        return CloudType.vCloud
    return None


def get_migration_target(s: str) -> MigrationTarget:
    if s == "null":
        return None
    json_ = json.loads(s)
    cloud_type = json_['cloud_type']['state']
    credentials = get_credentials(json.dumps(json_['cloud_credentials']))
    target_vm = get_workload(json.dumps(json_['target_vm']))
    return MigrationTarget(cloud_type, credentials, target_vm)


def get_migration_state(s: str) -> MigrationState:
    if s == "null":
        return None
    if s == "NOT_STARTED":
        return MigrationState.NOT_STARTED
    if s == "RUNNING":
        return MigrationState.RUNNING
    if s == "ERROR":
        return MigrationState.ERROR
    if s == "SUCCESS":
        return MigrationState.SUCCESS


def get_migration(s: str) -> Migration:
    if s == "null":
        return None

    json_ = json.loads(s)
    mount_points = [get_mount_point(json.dumps(s)) for s in json_['mount_points']]
    source = get_workload(json.dumps(json_['source']))
    migration_target = get_migration_target(json.dumps(json_['migration_target']))
    migration_state = get_migration_state(json_['migration_state']['state'])
    migration = Migration(mount_points, source, migration_target)
    migration.migration_state = migration_state
    return migration
