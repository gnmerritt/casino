import datetime
from sqlalchemy.sql import func
from models import MatchResult, BotSkill, BotRank, BotIdentity


class SkillUpdater(object):
    def run(self, db):
        session = db.session
        today = datetime.date.today()
        skills = session.query(
            BotIdentity.id,
            func.coalesce(func.sum(MatchResult.delta_chips), 0),
            func.coalesce(func.sum(MatchResult.hands), 0),
            ) \
            .outerjoin(MatchResult) \
            .group_by(BotIdentity.id) \
            .all()
        yesterday = today - datetime.timedelta(days=1)
        yesterdays_skills = {b.bot: b.skill for b in
                             BotSkill.query.filter_by(date=yesterday).all()}
        BotSkill.query.filter_by(date=today).delete()
        session.bulk_save_objects(
            [BotSkill(s[0], today,
                      self.calc_winnings_per_hand(s[1], s[2]),
                      yesterdays_skills.get(s[0], 0))
             for s in skills]
        )
        session.commit()

    def calc_winnings_per_hand(self, chips, hand):
        try:
            return chips / hand
        except ZeroDivisionError:
            return 0


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
