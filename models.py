from libs.google.appengine.ext import ndb


DEFAULT_NAME_KEY = 'key_shop'


class Cat(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    whiskers = ndb.StringProperty(indexed=False)


class Store(ndb.Model):
    business = ndb.StringProperty(indexed=False)
    owner = ndb.StringProperty(indexed=True)


class ConstructKey():
    def __init__(self, name=DEFAULT_NAME_KEY):
        self._name = name

    def create_key(self):
        key = ndb.Key('Store', self._name)
        return ndb.Key('Store', self._name)