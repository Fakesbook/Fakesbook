from os import environ, urandom
from sys import argv
from base64 import b64encode
from privacy_app import app
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

if __name__ == '__main__':

    port = 8080
    debugPort = 8081

    if len(argv) > 1 and argv[1] == "debug":
        app.run(debug=True, port=debugPort)
    else:
        flask_site = WSGIResource(reactor, reactor.getThreadPool(), app)
        reactor.listenTCP(port, Site(flask_site))
        reactor.run()
