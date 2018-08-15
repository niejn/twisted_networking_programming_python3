from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

class Greeter(Protocol):
    def connectionMade(self):
        self.transport.write(b"Hello server, I am the client!\r\n")
        print("Hello server, I am the client!\r\n")

    def sendMessage(self, msg):
        # self.transport.write(b"Hello server, I am the client2!\r\n")
        self.transport.write(b"Client said: %s" % msg)
        print("Client said: %s" % msg)
    #
    def dataReceived(self, data):
        print(b"Server said: %s" % data)
        # self.transport.write(b"Hello server, I am the client3!\r\n")



def gotProtocol(p):
    p.sendMessage(b"Hello")
    reactor.callLater(1, p.sendMessage, b"This is sent in a second")
    reactor.callLater(2, p.transport.loseConnection)

point = TCP4ClientEndpoint(reactor, "localhost", 8000)
d = connectProtocol(point, Greeter())
d.addCallback(gotProtocol)
reactor.run()