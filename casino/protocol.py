from twisted.protocols import basic
from twisted.python import log

import handlers


class CommandHandler(object):
    CMD = "!"

    def __init__(self, parent, api_url):
        self.parent = parent
        self.fx_login = handlers.LoginHandler(api_url)

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
            log.err()


class PokerProtocol(basic.LineReceiver):
    SPAM_LIMIT = 20
    delimiter = "\n"

    def connectionMade(self):
        self.authenticated = False
        self.non_auth_lines = 0
        self.handler = CommandHandler(self, self.factory.api_url)

    def connectionLost(self, reason):
        log.msg("Connection lost: {}".format(reason))

    def lineReceived(self, line):
        self.handler.handle(line)
        if self.authenticated:
            self.factory.bot_said(self, line)
        else:
            self.sendLine('!! All input is ignored until you log in.')
            self.non_auth_lines += 1
            if self.non_auth_lines > self.SPAM_LIMIT:
                self.closeBecause("You need to log in")

    def login_success(self, match, bot):
        self.authenticated = True
        self.game = match
        self.bot = bot
        self.factory.bot_said(self, "!joining")

    def closeBecause(self, reason):
        self.sendLine('!! CLOSING CONNECTION BECAUSE "{}"'.format(reason))
        self.transport.loseConnection()
