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
        }


BOTS_PER_USER = 1

class BotMaker(object):
    def __init__(self, user, name):
        self.user = user
        self.bot = BotIdentity(user, name)

    def create(self, db):
        data = PlayerData(self.user)
        if len(data.bots) >= BOTS_PER_USER:
            raise Exception("Already have too many bots")
        db.session.add(self.bot)
        db.session.commit()
        return serialize(self.bot)
