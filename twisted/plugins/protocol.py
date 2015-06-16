from twisted.protocols import basic
from twisted.python import log


class PokerProtocol(basic.LineReceiver):
    def connectionMade(self):
        log.msg("Connection made!")

    def connectionLost(self, reason):
        log.msg("Connection lost: {}".format(reason))

    def lineReceived(self, line):
        log.msg("Got line :: {}".format(line))
