from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol


class QuoteProtocol(protocol.Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numConnections += 1

    def dataReceived(self, data):
        print("Number of connections: %d"
              % self.factory.numConnections)
        print('Received:')
        print(data)
        print('MY Quote:')
        print(self.getQuote())
        self.transport.write(self.getQuote())
        self.updateQuote(data)

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

    def getQuote(self):
        return self.factory.quote

    def updateQuote(self, quote):
        self.factory.quote = quote


class QuoteFactory(Factory):
    numConnections = 0

    def __init__(self, quote=None):
        self.quote = quote or b"An apple a day"

    def buildProtocol(self, addr):
        return QuoteProtocol(self)


reactor.listenTCP(8000, QuoteFactory())
reactor.run()