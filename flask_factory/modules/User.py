

class User:

    def __init__(self, id_user, username, password) -> None:
        self.attributes = {
            "id": id_user,
            "username": username,
            "password": password
        }

    def show(self):
        print(self.attributes)