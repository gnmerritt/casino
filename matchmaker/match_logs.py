import json
import os

from matchmaker import app
from display import DisplayBot, DisplayResults
from models import Match, Player, MatchResult
from util import serialize

LOGS_FOLDER = app.config['MATCH_LOGS']

class MatchLogBuilder(object):
    def __init__(self, match_id):
        self.match = Match.query.get(match_id)
        self.players = [DisplayBot(p.bot).json()
                        for p in Player.query.filter_by(match=match_id).all()]
        self.results = DisplayResults(
            MatchResult.query.filter_by(match=match_id).all())

    def valid(self):
        return self.match and self.match.finished

    def read_hands(self):
        folder = LOGS_FOLDER + self.match.guid
        logs = []
        for root, dirs, files in os.walk(folder):
            for f in files:
                path = os.path.join(root, f)
                logs.append(self.get_json(path))
        return logs

    def get_json(self, filename):
        try:
            with open(filename, 'r') as myfile:
                text = myfile.read().replace('\n', '')
                return json.loads(text)
        except IOError:
            app.logger.error("Exploded reading logs for match {}"
                             .format(self.match.id))

    def data(self):
        return {
            "players": self.players,
            "match": serialize(self.match),
            "results": self.results.json(),
            "hands": self.read_hands()
        }
