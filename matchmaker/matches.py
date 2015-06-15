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
        self.game = Match.query.filter_by(guid=game).first()
        self.bot = BotIdentity.query.filter_by(key=bot).first()

    def join(self, db):
        if self.game.players() >= self.MAX_PLAYERS:
            raise Exception("Too many players")
        if self.bot is None:
            raise Exception("Invalid bot key")
        if self.game is None:
            raise Exception("Invalid match key")

        player = Player(self.bot, self.game.id)
        db.session.add(player)
        db.session.commit()
