from twisted.internet.protocol import ServerFactory

from protocol import PokerProtocol

class PokerFactory(ServerFactory):
    protocol = PokerProtocol

    def __init__(self, service):
        self.service = service
