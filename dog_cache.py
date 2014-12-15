from libs.google.appengine.api import memcache
from models import Dog, KeyDog

KEYNAME = '_name'
KEYTYPE = '_type'
PREFIXKEY = 'dog_'


class DogMemcache():
    def __init__(self):
        self._memcache = memcache.Client()
        self._key = KeyDog().create_key()

    def _set_cache_name(self, dog_id, name):
        try:
            dog_id += KEYNAME
            self._memcache.add(dog_id, name)
        except Exception as e:
            raise Exception(e.message)

    def _set_cache_type(self, dog_id, tipo):
        try:
            dog_id += KEYTYPE
            self._memcache.add(dog_id, tipo)
        except Exception as e:
            raise Exception(e.message)
        
    def _get_cache_dog(self, key):
        return self._memcache.get(key=key)

    def setdog_cache(self, list_dogs):
        try:
            self._memcache.add(self._key.name(), list_dogs, time=60)
        except Exception as e:
            raise Exception(e.message)

    def getdog_cache(self, key):
        dog_list = self._memcache.get(key=key.name())

        return dog_list

    def get_cache_misses(self):
        return self._memcache.get_stats()['misses']

    def get_cache_hits(self):
        return self._memcache.get_stats()['hits']
