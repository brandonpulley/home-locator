from gevent.wsgi import WSGIServer
from server import app

http_server = WSGIServer(('', 8080), app)
http_server.serve_forever()
