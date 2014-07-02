from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
import settings
import requests
from flask import Flask
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.debug = False

if not app.debug:
    import logging
    file_handler = logging.FileHandler('production.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

socketio = SocketIO(app)
thread = None

class StorjAPI:
	def __init__(self):
		self.node = app.config['NODE_URL']
		self.statusPath = '/api/status'
	@staticmethod
	def getNodeStatus():
		r = requests.get(self.node + statusPath)
		return r.json()

def status_thread():
    while True:
        time.sleep(10)
        socketio.emit('status', StorjAPI.getNodeStatus(), namespace='/metadisk')

@socket.io('status')
def node_status():
	socketio.emit('status', StorjAPI.getNodeStatus())

@socketio.on('connect', namespace='/metadisk')
def metadisk_connect():
	global thread
    if thread is None:
        thread = Thread(target=status_thread)
        thread.start()
    print('Client has connected.')

@socketio.on('disconnect', namespace='/metadisk')
def metadisk_disconnect():
    print('Client has disconnected.')


if __name__ == '__main__':
	socketio.run(app)