import logging

from flask import Flask, request, jsonify
from gevent.wsgi import WSGIServer

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)
app.logger.disabled = False
log = app.logger

# load routes
from server import routes

http_server = WSGIServer(('', 8080), app)
http_server.serve_forever()
