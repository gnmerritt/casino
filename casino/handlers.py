from twisted.internet import reactor
from twisted.python import log
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

agent = Agent(reactor)


class LoginHandler(object):
    def handle(self, handler, args):
        game, bot = args
        self.handler = handler
        self.game = game
        self.bot = bot

        def failed(ignored):
            self.handler.parent.closeBecause("login failed")

        def http_succeeded(response):
            if response.code != 200:
                failed(response)
            else:
                log.msg("login succeeded")
                self.handler.parent.authenticated = True

        # TODO: move this to a config file
        url = 'http://localhost:5000/api/internal/join/{}?key={}'\
              .format(self.game, self.bot)
        d = agent.request(
            'POST', url,
            Headers({'User-Agent': ['Plumbing Connector']}), None
        )
        d.addCallbacks(http_succeeded, failed)
