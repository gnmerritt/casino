from twisted.application import service
from twisted.python import log

from arena import ArenaHolder


class PokerService(service.Service):
    def __init__(self, api_url, log_dir):
        self.api_url = api_url
        self.log_dir = log_dir

    def startService(self):
        log.msg("PokerService service started")
        self.matches = ArenaHolder(self.api_url, self.log_dir)
