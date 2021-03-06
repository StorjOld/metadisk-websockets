from gevent import monkey
monkey.patch_all()

import time
from datetime import datetime
from threading import Thread
import settings
import requests
from flask import Flask, request
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config.from_object('settings')
app.debug = False

if not app.debug:
    import logging
    file_handler = logging.FileHandler('production.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

socketio = SocketIO(app)
thread = None

class StorjAPI:
	@staticmethod
	def getNodeStatus():
		r = requests.get(app.config['NODE_URL'] + '/api/status')
		return r.json()

def status_thread():
    while True:
        time.sleep(5)
        socketio.emit('status', StorjAPI.getNodeStatus(), namespace='/metadisk')

@socketio.on('connect', namespace='/metadisk')
def metadisk_connect():
	socketio.emit('status', StorjAPI.getNodeStatus(), namespace='/metadisk')
	global thread
	if thread is None:
		thread = Thread(target=status_thread)
		thread.start()
	print('Client has connected from ' + request.remote_addr + ' at ' + str(datetime.now()))

@socketio.on('disconnect', namespace='/metadisk')
def metadisk_disconnect():
    print('Client has disconnected from ' + request.remote_addr + ' at ' + str(datetime.now()))

if __name__ == '__main__':
	socketio.run(app, host='127.0.0.1', port=5050)