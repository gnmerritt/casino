import datetime
from sqlalchemy.sql import func
from models import MatchResult, BotSkill, BotRank


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


class RankUpdater(object):
    def run(self, db):
        BotRank.query.delete()
        today = datetime.date.today()
        skills = BotSkill.query.filter_by(date=today) \
            .order_by(BotSkill.skill.desc()) \
            .all()
        for i, skill in enumerate(skills, 1):
            rank = BotRank(skill.bot, i)
            db.session.add(rank)
        db.session.commit()
