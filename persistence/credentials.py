import os
from migration.credentials import Credentials
from migration.json_decoder import get_credentials
from .jsonpickler import JsonPickler

SCRIPT_PATH = os.path.dirname(__file__)
CREDENTIALS_DIRNAME = os.path.join(SCRIPT_PATH, "credentials")


class CredentialsPickler(JsonPickler):
    def __init__(self, dirname = CREDENTIALS_DIRNAME):
        super().__init__(dirname=dirname)

    def get_id(self, credentials: Credentials) -> str:
        ret = credentials.username + credentials.password
        if credentials.domain is not None:
            ret += credentials.domain

        return ret

    def get_serializable(self, s: str) -> Credentials:
        return get_credentials(s)

    def is_possible_to_create(self, obj: object) -> (bool, str):
        return True, ""

    def is_possible_to_update(self, old_obj: object, new_obj: object) -> (bool, str):
        return True, ""

    def fits(self, pickle_object: Credentials, object: Credentials) -> bool:
        if pickle_object is not None and object is not None:
            if pickle_object.username != object.username or pickle_object.password != object.password:
                return False

            if object.domain is not None:
                if object.domain != pickle_object.domain:
                    return False
        else:
            return pickle_object is None and object is None

        return True
