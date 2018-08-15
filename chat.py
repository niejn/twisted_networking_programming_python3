from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, protocol

'''
my_str = "hello world"
my_str_as_bytes = str.encode(my_str)
type(my_str_as_bytes) # ensure it is byte representation
my_decoded_str = my_str_as_bytes.decode()
type(my_decoded_str) # ensure it is string representation
'''

class Chat(protocol.Protocol):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.transport.write(b"What's your name?")
        # self.sendLine(b"What's your name?")

    def dataReceived(self, data):
        print("Client said: %s" % data)
        self.transport.write(data)





class ChatFactory(Factory):

    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)


reactor.listenTCP(8123, ChatFactory())
reactor.run()