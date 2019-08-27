class MountPoint:
    def __init__(self, mount_point_name: str, size: int):
        self.mount_point_name = mount_point_name
        self.size = size

    def repr_json(self):
        return dict(mount_point_name=self.mount_point_name, size=self.size)