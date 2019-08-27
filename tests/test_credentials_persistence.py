import unittest
import os

from migration.credentials import Credentials

from persistence.credentials import CredentialsPickler

SCRIPT_PATH = os.path.dirname(__file__)
CREDENTIALS_DIRNAME = os.path.join(SCRIPT_PATH, "credentials")

credentials_pickler = CredentialsPickler(dirname=CREDENTIALS_DIRNAME)


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
       for filename in os.listdir(CREDENTIALS_DIRNAME):
           os.remove(os.path.join(CREDENTIALS_DIRNAME, filename))

    def test_create_and_read_one_record(self):
        credentials1 = Credentials("username", "password", "domain")
        credentials_pickler.create(credentials1)

        credentials2 = Credentials("username", "password", None)
        credentials_pickler.create(credentials2)

        ret = credentials_pickler.read(credentials1)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].username, "username")
        self.assertEqual(ret[0].password, "password")
        self.assertEqual(ret[0].domain, "domain")

    def test_create_and_read_several_records(self):
        credentials1 = Credentials("username", "password", "domain")
        credentials_pickler.create(credentials1)

        credentials2 = Credentials("username", "password", None)
        credentials_pickler.create(credentials2)

        ret = credentials_pickler.read(credentials2)
        self.assertEqual(len(ret), 2)

    def test_update_one_record(self):
        credentials = Credentials("user", "qwerty", None)
        credentials_pickler.create(credentials)
        new_credentials = Credentials("user", "qwerty", "domain")
        credentials_pickler.update(credentials, new_credentials)
        ret = credentials_pickler.read(new_credentials)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].username, "user")
        self.assertEqual(ret[0].password, "qwerty")
        self.assertEqual(ret[0].domain, "domain")

    def test_update_several_records(self):
        credentials1 = Credentials("user", "qwerty", "domain1")
        credentials_pickler.create(credentials1)

        credentials2 = Credentials("user", "qwerty", "domain2")
        credentials_pickler.create(credentials2)

        credentials3 = Credentials("user", "qwerty", "domain")
        credentials_to_update = Credentials("user", "qwerty", None)
        credentials_pickler.update(credentials_to_update, credentials3)
        ret = credentials_pickler.read(credentials_to_update)
        self.assertEqual(len(ret), 2)
        self.assertEqual(ret[0].username, "user")
        self.assertEqual(ret[0].password, "qwerty")
        self.assertEqual(ret[1].username, "user")
        self.assertEqual(ret[1].password, "qwerty")
        self.assertEqual(ret[0].domain, "domain")
        self.assertEqual(ret[1].domain, "domain")

    def test_delete(self):
        credentials1 = Credentials("user", "password", "domain1")
        credentials_pickler.create(credentials1)
        credentials2 = Credentials("user", "password", "domain2")
        credentials_pickler.create(credentials2)

        credentials_to_delete = Credentials("user", "password", None)
        credentials_pickler.delete(credentials_to_delete)
        self.assertEqual(credentials_pickler.read(credentials_to_delete), [])


if __name__ == '__main__':
    unittest.main()

