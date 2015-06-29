from twisted.application import service
from twisted.python import log

from arena import ArenaHolder


class PokerService(service.Service):
    def startService(self):
        log.msg("PokerService service started")
        self.matches = ArenaHolder()
