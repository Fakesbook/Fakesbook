from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from privacy_app import app

PORT = 8080

flask_site = WSGIResource(reactor, reactor.getThreadPool(), app)
reactor.listenTCP(PORT, Site(flask_site))
reactor.run()
