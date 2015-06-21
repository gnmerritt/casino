from models import Match, BotIdentity, Player
from util import serialize


class OpenMatches(object):
    def __init__(self, db):
        self.matches = Match.query.filter_by(active=True).all()

    def active(self):
        return [serialize(m) for m in self.matches]


class NewMatch(object):
    def create(self, db, active=True):
        self.match = Match()
        self.match.active = active
        db.session.add(self.match)
        db.session.commit()

    def guid(self):
        return self.match.guid

class MatchJoiner(object):
    MAX_PLAYERS = 2 # hardcoded for meow

    def __init__(self, game, bot):
        self.match = Match.query.filter_by(guid=game).first()
        self.bot = BotIdentity.query.filter_by(key=bot).first()

    def join(self, db):
        if self.bot is None:
            return 401, "Invalid bot key"
        if self.match is None:
            return 404, "Invalid match key"
        if self.match.players() >= self.MAX_PLAYERS:
            return 410, "Too many players"

        player = Player(self.bot, self.match)
        db.session.add(player)
        db.session.commit()
        return 200, "Joined"
