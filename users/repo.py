from . import user


class InMemoryUsersRepo(user.UserRepo):
    def __init__(self):
        self.next_id = 1
        self.by_id = dict()

    def get_all(self):
        return tuple(self.by_id.values())

    def get_by_id(self, id):
        return self.by_id.get(id, None)

    def get_by_name(self, name):
        for _, value in self.by_id.items():
            if value.username == name:
                return value
        return None

    def request_create(self, name, password):
        found = self.get_by_name(name)
        if not (found is None):
            return None  # пользователь с таким именем уже есть
        new_user = user.User(id=self.next_id, username=name, password=password)
        self.by_id[self.next_id] = new_user
        self.next_id += 1
        return new_user

    def request_update(self, id, name, password):
        found = self.get_by_id(id)
        if found is None:
            return
        found.name = name
        found.password = password

    def request_delete(self, id):
        self.by_id.pop(id, None)

    def authorize(self, login, password):
        user = self.get_by_name(login)
        if user is None:
            return None, "no user"
        if user.password != password:
            return None, "bad password"
        return user, ""
