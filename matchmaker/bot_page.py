from flask import abort

from matchmaker import db
from models import User, BotIdentity, MatchResult, BotSkill, BotRank


class BotData(object):
    def __init__(self, bot_id):
        self.bot = None
        try:
            self.bot = BotIdentity.query.get(bot_id)
        except:
            db.session.rollback()
        if not self.bot:
            self.bot = BotIdentity.query \
                .filter(BotIdentity.guid == bot_id) \
                .first()
        if not self.bot:
            abort(404)
        self.owner = User.query.get(self.bot.user_id)
        games = MatchResult.query \
            .filter(MatchResult.bot == self.bot.id) \
            .order_by(MatchResult.timestamp.desc()) \
            .limit(50) \
            .all()
        skill = BotSkill.query.filter(BotSkill.bot == self.bot.id).first()
        self.skill = skill.skill
        self.delta = skill.delta
        self.rank = BotRank.query.filter(BotRank.bot == self.bot.id) \
            .first().rank
        self.num_bots = BotIdentity.query.count()
        self.games = [{
            "guid": g.match, "ts": g.timestamp, "delta_chips": g.delta_chips,
            "name": self.bot.name, "hands": g.hands
        } for g in games]

    def data(self):
        return {
            "bot": self.bot,
            "owner": self.owner.username,
            "skill": self.skill,
            "delta": self.delta,
            "rank": self.rank,
            "games": self.games,
            "bots": self.num_bots
        }
