from twisted.internet import reactor
from twisted.python import log
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

agent = Agent(reactor)


class LoginHandler(object):
    def __init__(self, api_url):
        self.api_url = api_url

    def handle(self, handler, args):
        game, bot = args

        def failed(ignored, reason="login failed"):
            handler.parent.closeBecause(reason)

        def http_succeeded(response):
            if response.code == 200:
                log.msg("login succeeded")
                try:
                    handler.parent.login_success(game, bot)
                except:
                    log.err()
            elif response.code == 401:
                failed(response, "Invalid bot key")
            elif response.code == 404:
                failed(response, "Invalid game")
            elif response.code == 410:
                failed(response, "Game is full")
            else:
                failed(response)

        url = '{}/api/internal/join/{}?key={}'\
              .format(self.api_url, game, bot)
        d = agent.request(
            'POST', url,
            Headers({'User-Agent': ['Plumbing Connector']}), None
        )
        d.addCallbacks(http_succeeded, failed)
