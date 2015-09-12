
from models import BotIdentity, BotSkill, BotRank


class BotInfo(object):
    def __init__(self, db, guid):
        db_bot = db.session.query(
            BotIdentity.name, BotIdentity.user_id, BotIdentity.guid,
            BotSkill.skill, BotRank.rank) \
            .outerjoin(BotSkill) \
            .outerjoin(BotRank) \
            .filter(BotIdentity.guid == guid) \
            .first()
        if db_bot:
            keys = ["name", "user_id", "guid", "skill", "rank"]
            self.bot = {keys[i]: val for i, val in enumerate(db_bot)}
