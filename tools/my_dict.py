class MyDict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, item):
        return self.get(item, None)

    def __init__(self, **kwargs):
        super(MyDict, self).__init__(**kwargs)
