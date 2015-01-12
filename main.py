#!/usr/bin/env python

import webapp2
from task import Task
from models import Mensaje


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Iniciando hilo')

        task = Task()
        try:
            task.start()
        except Exception as e:
            self.response.write(e.message)
        finally:
            self.response.write('<br>Fin del hilo')


class TaskHandler(webapp2.RequestHandler):
    def post(self):
        var1 = self.request.get('param1')

        if type(var1) != 'str' or type(var1) != 'unicode':
            var1 = '%s' % var1

        import time
        time.sleep(120)

        mensaje = Mensaje()
        mensaje.contenido = var1
        mensaje.put()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/task', TaskHandler),
], debug=True)
