from twisted.internet.protocol import ServerFactory

from protocol import PokerProtocol
from arena import ArenaHolder


class PokerFactory(ServerFactory):
    protocol = PokerProtocol

    def __init__(self, service):
        self.service = service
        self.matches = ArenaHolder()

    def bot_said(self, protocol, line):
        match_key = protocol.game
        bot = protocol.bot
        match = self.matches.get_or_create(match_key)
        if match:
            match.add_bot(bot, protocol) # usually a no-op
            if line:
                match.bot_said(bot, line)
        else:
            protocol.closeBecause("Game has ended")
