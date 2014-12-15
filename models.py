from libs.google.appengine.ext import db

DOGKEYNAME = 'default'


class Dog(db.Model):
    name = db.StringProperty(indexed=True)
    type = db.StringProperty(indexed=False)


class KeyDog(db.Key):
    @staticmethod
    def create_key():
        return db.Key.from_path('Dog', DOGKEYNAME)