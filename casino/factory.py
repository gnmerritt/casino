from twisted.internet.protocol import ServerFactory

from protocol import PokerProtocol


class PokerFactory(ServerFactory):
    protocol = PokerProtocol

    def __init__(self, service, api_url):
        self.service = service
        self.api_url = api_url

    def bot_said(self, protocol, line):
        match_key = protocol.game
        bot = protocol.bot
        match = self.service.matches.get_or_create(match_key)
        if match:
            match.add_bot(bot, protocol)  # usually a no-op
            if line:
                match.bot_said(bot, line)
        else:
            protocol.closeBecause("Game has ended")
