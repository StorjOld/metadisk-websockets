metadisk-websockets
===================

A small python module that wraps Storj API calls with Flask-SocketIO.

The module is designed to be completely independent from other storj web-core libraries. It interacts with the API through `requests` calls. The node URL is specified in a local settings file.

## Deployment

Running with `python index.py` will launch application using gevent-socketio web server. Alternatively, you can use gunicorn with `gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker metadisk-websockets:app`.

## Using nginx as WebSocket Reverse Proxy
Flask-SocketIO recommends the following example configuration on nginx 1.4+:
```
server {
    listen 80;
    server_name localhost;
    access_log /var/log/nginx/example.log;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_redirect off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /socket.io {
        proxy_pass http://127.0.0.1:5000/socket.io;
        proxy_redirect off;
        proxy_buffering off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}
```

## Compatibility

Only compatible with Python 2.x due to Flask-SocketIO's gevent dependency.
