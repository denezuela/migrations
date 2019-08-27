class Credentials:
    def __init__(self, username: str, password: str, domain: str):
        if username is not None:
            self._username = username
        else:
            raise TypeError("Username should not be None")

        if password is not None:
            self._password = password
        else:
            raise TypeError("Password should not be None")

        self.domain = domain

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if value is not None:
            self._username = value
        else:
            raise AttributeError("Username should not be None")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if value is not None:
            self._password = value
        else:
            raise AttributeError("Username should not be None")

    def repr_json(self):
        return dict(username=self.username, password=self.password, domain=self.domain)