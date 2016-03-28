from util import serialize
from models import BotIdentity, BotRank


class DisplayBot(object):
    """A BotIdentity with some relevant joins"""
    def __init__(self, bot_id):
        self.bot = BotIdentity.query.get(bot_id)
        rank = BotRank.query.get(bot_id)
        self.rank = rank.rank if rank else None

    def json(self):
        return {
            "bot": serialize(self.bot, scrub=["key"]),
            "rank": self.rank
        }


class DisplayResults(object):
    def __init__(self, results):
        self.results = results

    def json(self):
        return {r.bot: serialize(r, scrub=["bot", "id"])
                for r in self.results}
