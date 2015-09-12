import datetime

from sqlalchemy import or_

from models import BotIdentity, MatchResult, BotSkill, BotRank
from util import serialize
from matchmaker import db


class PlayerData(object):
    def __init__(self, user):
        today = datetime.date.today()
        self.bots = db.session.query(
            BotIdentity.name, BotIdentity.id, BotIdentity.user_id,
            BotIdentity.guid, BotIdentity.key, BotSkill.skill,
            BotRank.rank) \
            .outerjoin(BotSkill) \
            .outerjoin(BotRank) \
            .filter(BotIdentity.user_id == user.id,
                    # Need to use '== None' for when the join is null
                    or_(BotSkill.date == today, BotSkill.date == None)) \
            .all()
        self.user = user
        bot_names = {b.id: b.name for b in self.bots}
        results = [] if not bot_names else MatchResult.query \
            .filter(MatchResult.bot.in_(bot_names.keys())) \
            .order_by(MatchResult.timestamp.desc()) \
            .limit(25).all()

        self.games = [{
            "guid": g.match, "ts": g.timestamp, "delta_chips": g.delta_chips,
            "name": bot_names[g.bot], "hands": g.hands
        } for g in results]

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
