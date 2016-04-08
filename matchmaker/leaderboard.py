import datetime

from sqlalchemy.sql.expression import and_

from models import BotIdentity, BotSkill, BotRank
from matchmaker import db


class Leaderboard(object):
    def __init__(self, user=None):
        owned_exp = and_(user is not None and hasattr(user, 'id')
                         and BotIdentity.user_id == user.id)
        self.bots = db.session.query(
            BotIdentity.name, BotIdentity.guid,
            BotSkill.skill, BotSkill.delta, BotRank.rank,
            BotSkill.games,
            owned_exp.label("owned")
            ) \
            .join(BotSkill) \
            .join(BotRank) \
            .filter(BotSkill.date == datetime.date.today()) \
            .order_by(BotRank.rank.asc()) \
            .limit(50) \
            .all()

    def data(self):
        return {"bots": self.bots}
