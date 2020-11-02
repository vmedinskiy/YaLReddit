from tools.my_dict import MyDict


class User(MyDict):
    pass


class UserRepo:
    def get_all(self):
        raise NotImplemented

    def get_by_id(self, id):
        raise NotImplemented

    def get_by_name(self, name):
        raise NotImplemented

    def request_create(self, name, password):
        raise NotImplemented

    def request_update(self, id, name, password):
        raise NotImplemented

    def request_delete(self, id):
        raise NotImplemented

    def authorize(self, login, password):
        raise NotImplemented
