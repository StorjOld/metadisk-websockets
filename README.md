metadisk-websockets
===================

A small python module that wraps Storj API calls with Flask-SocketIO.

The module is designed to be completely independent from other storj web-core libraries. It interacts with the API through `requests` calls. The node URL is specified in a local settings file.

## Deployment

Running with `python index.py` will launch application using gevent-socketio web server. Alternatively, you can use gunicorn with `gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker metadisk-websockets:app`.

## Compatibility

Only compatible with Python 2.x due to Flask-SocketIO's gevent dependency.
