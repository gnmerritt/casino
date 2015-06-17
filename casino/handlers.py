

class LoseConnectionException(Exception):
    """Thrown by handlers to indicate that the parent should close
    the connection down immediately"""
    pass


class LoginHandler(object):
    def handle(self, handler, args):
        self.login(handler) # TODO actually check

    def login(self, handler):
        handler.parent.authenticated = True
