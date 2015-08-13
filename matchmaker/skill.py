import datetime
from sqlalchemy.sql import func
from models import MatchResult, BotSkill


class SkillUpdater(object):
    def run(self, db):
        session = db.session
        today = datetime.date.today()
        skills = session.query(
            MatchResult.bot,
            func.sum(MatchResult.delta_chips),
            func.sum(MatchResult.hands)
            ) \
          .group_by(MatchResult.bot) \
          .all()
        BotSkill.query.filter_by(date=today).delete()
        session.bulk_save_objects(
            [BotSkill(s[0], today, s[1] / s[2])
             for s in skills]
        )
        session.commit()
