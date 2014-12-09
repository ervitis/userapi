from libs.google.appengine.api import memcache


class Repository():
    def __init__(self, cursor):
        self._memcache = memcache
        self._cursor = cursor