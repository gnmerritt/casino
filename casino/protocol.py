from twisted.protocols import basic
from twisted.python import log

import handlers


class CommandHandler(object):
    CMD = "!"

    fx_login = handlers.LoginHandler()

    def __init__(self, parent):
        self.parent = parent

    def handle(self, line):
        """Dispatches to functions for lines starting with !
        e.g. '!login nathan' -> self.fx_login([nathan])
        """
        if not line.startswith(self.CMD):
            return
        try:
            command, _, args = line[1:].partition(" ")
            args = args.split(None)
            getattr(self, 'fx_{}'.format(command)).handle(self, args)
        except:
            log.msg("generic error after handle")
            pass


class PokerProtocol(basic.LineReceiver):
    SPAM_LIMIT = 20
    delimiter = "\n"

    def connectionMade(self):
        self.authenticated = False
        self.non_auth_lines = 0
        self.handler = CommandHandler(self)

    def connectionLost(self, reason):
        log.msg("Connection lost: {}".format(reason))

    def lineReceived(self, line):
        log.msg("Got line :: {}".format(line))
        self.handler.handle(line)
        if self.authenticated:
            pass # TODO: send line to arena
        else:
            self.sendLine('!! All input is ignored until you log in.')
            self.non_auth_lines += 1
            if self.non_auth_lines > self.SPAM_LIMIT:
                self.closeBecause("You need to log in")

    def closeBecause(self, reason):
        self.sendLine('!! CLOSING CONNECTION BECAUSE "{}"'.format(reason))
        self.transport.loseConnection()
