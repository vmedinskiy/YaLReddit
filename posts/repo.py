import datetime

from . import post


class InMemoryPostsRepo(post.PostRepo):
    def __init__(self):
        self.next_id = 1
        self.by_id = dict()

    def get_all(self):
        return tuple(self.by_id.values())

    def get_by_id(self, id):
        return self.by_id.get(id, None)

    def get_by_user_login(self, login):
        result = list()
        for _, value in self.by_id.items():
            if value.author.username == login:
                result.append(value)
        return result

    def get_by_category(self, cat):
        result = list()
        for _, value in self.by_id.items():
            if value.category == cat:
                result.append(value)
        return result

    def request_create(self, post):
        post.id = self.next_id
        post.created = datetime.datetime.now()
        self.by_id[post.id] = post
        self.next_id += 1
        return post

    def request_update(self, post):
        return

    def request_delete(self, id, user):
        p = self.get_by_id(id)
        if not p:
            return f"post does not exist for id: {id}"
        if p.author.id != user.id:
            return f"you are not author of this post id: {id}"
        del self.by_id[id]
        return None

