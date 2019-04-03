from os import environ, urandom
from sys import argv
from base64 import b64encode
from privacy_app import app
from twisted.internet import tksupport, reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from appJar import gui

port = 8080
debugPort = 8081

def launchApp():
    flask_site = WSGIResource(reactor, reactor.getThreadPool(), app)
    reactor.listenTCP(port, Site(flask_site))
    reactor.run()

def stopApp():
    reactor.stop()

def launchDebug():
    app.run(debug=True, port=debugPort)

def buildGUI():
    appgui = gui("Fakesbook", "400x400")

    tksupport.install(appgui.topLevel)

    appgui.addLabel("title", "Fakesbook")
    appgui.buttons(["Launch", "Stop"], [launchApp, stopApp])

    appgui.go()

if __name__ == '__main__':

    if len(argv) > 1 and argv[1] == "debug":
        launchDebug()
    else:
        buildGUI()
