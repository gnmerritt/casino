from models import Match
from util import serialize


class OpenMatches(object):
    def __init__(self, db):
        self.matches = Match.query.filter_by(active=True).all()

    def active(self):
        return [serialize(m) for m in self.matches]
