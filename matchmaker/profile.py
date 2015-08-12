from models import Player, BotIdentity
from util import serialize


class PlayerData(object):
    def __init__(self, user):
        self.bots = BotIdentity.query.filter_by(user_id=user.id).all()
        self.user = user
        self.games = []

    def data(self):
        return {
            "user": self.user,
            "bots": self.bots,
            "games": self.games,
            "canAdd": self.user.max_bots > len(self.bots)
        }


class BotMaker(object):
    def __init__(self, user, name):
        self.user = user
        self.bot = BotIdentity(user, name)

    def create(self, db):
        data = PlayerData(self.user)
        if len(data.bots) >= self.user.max_bots:
            raise Exception("Already have too many bots")
        db.session.add(self.bot)
        db.session.commit()
        return serialize(self.bot)
