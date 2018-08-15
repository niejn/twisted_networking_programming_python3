from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("Hello server, I am the client!\r\n")

    def dataReceived(self, data):
        print("Server said: %s" % data)
        self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

reactor.connectTCP("localhost", 8000, EchoFactory())
reactor.run()
