from twisted.application import service
from twisted.python import log


class PokerService(service.Service):
    def startService(self):
        log.msg("PokerService service started")
