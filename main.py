#!/usr/bin/env python

import webapp2
import cgi
import time
from models import Dog, KeyDog
from dog_cache import DogMemcache

TEMPLATE_FORM = """
<html><head></head><body>
<form action='/sign' method='post'>
Nombre: <input type='text' name='txtNombre'><br>
Tipo perro: <input type='text' name='txtTipo'><br>
<button type='submit'>Guardar</button>
</form><br>
"""

TEMPLATE_END = """
</body></html>
"""

SLEEP = 0.2

dog_cache = DogMemcache()
KEY = 'dog_'


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(TEMPLATE_FORM)

        key = KeyDog().create_key()

        list_dogs = dog_cache.getdog_cache(key=key)
        if list_dogs:
            for dog in list_dogs:
                self.response.write('<br>Cached: %s is a %s' % (cgi.escape(dog.name), cgi.escape(dog.type)))
        else:
            dogs = Dog().all()
            dog_cache.setdog_cache(list_dogs=dogs)

        list_dogs = dog_cache.getdog_cache(key=key)
        for dog in list_dogs:
            self.response.write('<br>%s is a %s' % (cgi.escape(dog.name), cgi.escape(dog.type)))

        self.response.write('<br><br>Missed: %s' % dog_cache.get_cache_misses())
        self.response.write(' - Hits: %s' % dog_cache.get_cache_hits())

        self.response.write(TEMPLATE_END)


class SignHandler(webapp2.RequestHandler):
    def post(self):
        nombre = self.request.get('txtNombre')
        tipo = self.request.get('txtTipo')

        if not nombre or '' == nombre:
            self.redirect('/')

        dog = Dog()
        dog.name = nombre
        dog.type = tipo
        dog.put()

        time.sleep(SLEEP)
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sign', SignHandler),
], debug=True)
