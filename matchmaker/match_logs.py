from display import DisplayBot, DisplayResults
from models import Match, Player, MatchResult
from util import serialize


class MatchLogBuilder(object):
    def __init__(self, match_id):
        print("getting match id={}".format(match_id))
        self.match = Match.query.get(match_id)
        self.players = [DisplayBot(p.bot).json()
                        for p in Player.query.filter_by(match=match_id).all()]
        self.results = DisplayResults(
            MatchResult.query.filter_by(match=match_id).all())

    def valid(self):
        print("valid? match={}".format(self.match))
        return self.match and self.match.finished

    def data(self):
        return {
            "players": self.players,
            "match": serialize(self.match),
            "results": self.results.json(),
            "logs": None
        }
