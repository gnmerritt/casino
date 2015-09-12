from sqlalchemy import or_

from models import BotIdentity, BotSkill, BotRank


class BotInfo(object):
    def __init__(self, db, guid_or_key):
        db_bot = db.session.query(
            BotIdentity.name, BotIdentity.user_id, BotIdentity.guid,
            BotSkill.skill, BotRank.rank) \
            .outerjoin(BotSkill) \
            .outerjoin(BotRank) \
            .filter(or_(BotIdentity.guid == guid_or_key,
                        BotIdentity.key == guid_or_key)) \
            .first()
        if db_bot:
            keys = ["name", "user_id", "guid", "skill", "rank"]
            self.bot = {keys[i]: val for i, val in enumerate(db_bot)}
