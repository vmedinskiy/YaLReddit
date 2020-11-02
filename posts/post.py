from tools.my_dict import MyDict
from users.user import User

'''
{author: {username: "Beeezle", id: "5d0c19fe9ba1373573f27219"}
category: "programming"
comments: []
created: "2019-06-20T23:44:01.640Z"
id: "5d0c1a419ba137182ef2721a"
score: 150
text: "Now lemme tell ya something, young blood."
title: "FizzleDizzle"
type: "text"
upvotePercentage: 79
views: 4102
votes: []
'''


class Post(MyDict):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.votes = []
        self.comments = []
        self.upvotePercentage = 100
        if self.author:
            self.author = User(**self.author)


class PostRepo:
    def get_all(self):
        raise NotImplemented

    def get_by_id(self, id):
        raise NotImplemented

    def get_by_user_login(self, login):
        raise NotImplemented

    def get_by_category(self, cat):
        raise NotImplemented

    def request_create(self, post):
        raise NotImplemented

    def request_update(self, post):
        raise NotImplemented

    def request_delete(self, id, user):
        raise NotImplemented
