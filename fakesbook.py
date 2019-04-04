from sys import argv
from privacy_app import create_app
from twisted.internet import tksupport, reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from appJar import gui
import socket

port = 8080
debugPort = 8081

appgui = gui("Fakesbook", "400x400")
app = create_app()

# install gui support in twisted
tksupport.install(appgui.topLevel)

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
    appgui.setLabel("address", "server is running on: " + getIPAddress() + ":" + str(port))
    flask_site = WSGIResource(reactor, reactor.getThreadPool(), app)
    reactor.listenTCP(port, Site(flask_site))
    reactor.run()

def stopApp():
    appgui.setLabel("address", "server will run on: " + getIPAddress() + ":" + str(port))
    reactor.stop()

def launchDebug():
    app.run(debug=True, port=debugPort)

def saveDatabase():
    pass

def loadDatabase():
    pass

def buildGUI():

    appgui.addLabel("title", "Fakesbook")
    appgui.buttons(["Save Database", "Load a Database"], [saveDatabase, loadDatabase])
    appgui.buttons(["Launch", "Stop"], [launchApp, stopApp])

    appgui.addLabel("address", "server will run on: " + getIPAddress() + ":" + str(port))

    appgui.go()

if __name__ == '__main__':

    if len(argv) > 1 and argv[1] == "debug":
        launchDebug()
    else:
        buildGUI()
