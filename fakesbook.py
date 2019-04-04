from os import environ, urandom
from sys import argv
from base64 import b64encode
from privacy_app import app
from twisted.internet import tksupport, reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from appJar import gui
import socket

port = 8080
debugPort = 8081

def getIPAddress():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('10.255.255.255', 1))
        ip = sock.getsockname()[0]
    except:
        ip = socket.gethostbyname(socket.gethostname())
    finally:
        sock.close()
    return ip

def launchApp():
    flask_site = WSGIResource(reactor, reactor.getThreadPool(), app)
    reactor.listenTCP(port, Site(flask_site))
    reactor.run()

def stopApp():
    reactor.stop()

def launchDebug():
    app.run(debug=True, port=debugPort)

def saveDatabase():
    pass

def loadDatabase():
    pass

def buildGUI():
    appgui = gui("Fakesbook", "400x400")

    tksupport.install(appgui.topLevel)

    appgui.addLabel("title", "Fakesbook")
    appgui.buttons(["Save Database", "Load Database"], [saveDatabase, loadDatabase])
    appgui.buttons(["Launch", "Stop"], [launchApp, stopApp])

    appgui.addLabel("address", getIPAddress())

    appgui.go()

if __name__ == '__main__':

    if len(argv) > 1 and argv[1] == "debug":
        launchDebug()
    else:
        buildGUI()
