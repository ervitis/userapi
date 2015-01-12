from libs.google.appengine.api import taskqueue
import time


class Task():

    def __init__(self):
        self._taskqueue = taskqueue

    def start(self):
        time.sleep(10)
        self._taskqueue.add(url='/task', params={'param1': 'Prueba2'})
