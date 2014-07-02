import settings
import requests
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)

if not app.debug:
    import logging
    file_handler = logging.FileHandler('production.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

socketio = SocketIO(app)

class StorjAPI:
	def __init__(self):
		self.node = app.config['NODE_URL']
		self.statusPath = '/api/status'
	@staticmethod
	def getNodeStatus():
		r = requests.get(self.node + statusPath)
		return r.json()

@app.route('/')
def index():
    return render_template('index.html')

@socket.io('status'):
def node_status():
	socketio.emit('status', StorjAPI.getNodeStatus())

@socketio.on('connect', namespace='/metadisk')
def metadisk_connect():
   print('Client has connected.')

@socketio.on('disconnect', namespace='/metadisk')
def metadisk_disconnect():
    print('Client has disconnected.')


if __name__ == '__main__':
	socketio.run(app)