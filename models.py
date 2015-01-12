from libs.google.appengine.ext import db

DEFAULT_NAME = 'key_mensaje'
KEY = 'mensaje'


class Mensaje(db.Model):
    contenido = db.StringProperty(indexed=True)

    def save_mensaje(self, contenido):
        if contenido is None:
            return None

        self.contenido = contenido
        self.put()


class ConstructKey():
    def __init__(self, name=DEFAULT_NAME):
        self._name = name
        self._key = db.Key(encoded=KEY)

    def create_key(self):
        return self._key

    @staticmethod
    def get_key():
        return KEY
