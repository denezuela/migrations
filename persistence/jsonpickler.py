import hashlib
import os
import json

from migration.serializable import Serializable
from migration.json_encoder import ComplexEncoder

class JsonPickler:
    def __init__(self, dirname: str):
        self.dirname = dirname
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def get_id(self, obj: Serializable) -> str:
        pass

    def get_serializable(self, s: str) -> Serializable:
        pass

    def get_pickle_filename(self, obj: object) -> str:
        return hashlib.md5(self.get_id(obj).encode()).hexdigest()

    def is_possible_to_create(self, obj: Serializable) -> (bool, str):
        print("MUST BE OVERRIDEN")
        pass

    def is_possible_to_update(self, old_obj: Serializable, new_obj: Serializable) -> (bool, str):
        print("MUST BE OVERRIDEN")
        pass

    def create(self, obj: Serializable):
        is_possible_to_create, message = self.is_possible_to_create(obj)
        if not is_possible_to_create:
            raise Exception(message)

        with open(os.path.join(self.dirname, self.get_pickle_filename(obj)), "w") as f:
            f.write(json.dumps(obj.repr_json(), cls=ComplexEncoder))

    def fits(self, pickle_object: Serializable, real_object: Serializable) -> bool:
        pass

    def read(self, obj: Serializable) -> [Serializable]:
        ret = []
        for filename in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, filename), "r") as f:
                current = self.get_serializable(f.read())

                if self.fits(current, obj):
                    ret.append(current)

        return ret

    def get_filenames(self, obj: Serializable) -> [Serializable]:
        ret = []
        for filename in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, filename), "r") as f:
                current = self.get_serializable(f.read())

                if self.fits(current, obj):
                    ret.append(filename)

        return ret

    def update(self, old_obj: Serializable, new_obj: Serializable):
        is_possible_to_update, message = self.is_possible_to_update(old_obj, new_obj)
        if not is_possible_to_update:
            raise Exception(message)

        filenames_to_update = self.get_filenames(old_obj)
        for filename in filenames_to_update:
            with open(os.path.join(self.dirname, filename), "w") as f:
                f.write(json.dumps(new_obj.repr_json(), cls=ComplexEncoder))

    def delete(self, obj: Serializable):
        filenames_to_delete = self.get_filenames(obj)

        for filename in filenames_to_delete:
            path = os.path.join(self.dirname, filename)

            if os.path.exists(path):
                os.remove(os.path.join(self.dirname, filename))