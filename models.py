from libs.google.appengine.ext import db


DEFAULT_NAME_KEY = 'key_shop'
KEY = 'Store'


class Cat(db.Model):
    name = db.StringProperty(indexed=True)
    whiskers = db.StringProperty(indexed=False)


class Store(db.Model):
    business = db.StringProperty(indexed=False)
    owner = db.StringProperty(indexed=True)


class ConstructKey():
    def __init__(self, name=DEFAULT_NAME_KEY):
        self._name = name
        self._key = db.Key(encoded=KEY)

    def create_key(self):
        return self._key

    @staticmethod
    def get_key():
        return KEY