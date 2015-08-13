from models import BotIdentity, MatchResult
from util import serialize


class PlayerData(object):
    def __init__(self, user):
        self.bots = BotIdentity.query.filter_by(user_id=user.id).all()
        self.user = user
        bot_names = {b.id: b.name for b in self.bots}
        results = MatchResult.query \
          .filter(MatchResult.bot.in_(bot_names.keys())) \
          .limit(25).all()

        self.games = [{ "guid": g.match, "ts": g.timestamp, "delta_chips": g.delta_chips,
                        "name": bot_names[g.bot], "hands": g.hands }
                      for g in results]

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
