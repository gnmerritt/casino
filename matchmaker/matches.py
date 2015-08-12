from models import Match, BotIdentity, Player, MatchResult
from util import serialize


class OpenMatches(object):
    def __init__(self, db):
        self.matches = Match.query.filter_by(active=True).all()

    def active(self, config):
        connection_info = {
            'host': config.get("CASINO_HOST", None),
            'port': config.get("CASINO_PORT", None),
        }
        return [serialize(m, extras=connection_info) for m in self.matches]


class NewMatch(object):
    def create(self, db, active=True):
        self.match = Match()
        self.match.active = active
        db.session.add(self.match)
        db.session.commit()

    def guid(self):
        return self.match.guid


class MatchJoiner(object):
    MAX_PLAYERS = 2 # hardcoded for meow

    def __init__(self, game, bot):
        self.match = Match.query.filter_by(guid=game).first()
        self.bot = BotIdentity.query.filter_by(key=bot).first()

    def join(self, db):
        if self.bot is None:
            return 401, "Invalid bot key"
        if self.match is None:
            return 404, "Invalid match key"
        if self.match.players() >= self.MAX_PLAYERS:
            return 410, "Too many players"

        if self.match.players() + 1 >= self.MAX_PLAYERS:
            self.match.active = False
            db.session.add(self.match)

        player = Player(self.bot, self.match)
        db.session.add(player)
        db.session.commit()
        return 200, "Joined"


class MatchCreatorJob(object):
    def __init__(self, db):
        self.db = db

    def run(self):
        matches = OpenMatches(self.db)
        if len(matches.matches) == 0:
            match = NewMatch()
            match.create(self.db)
            return match.guid()


class MatchResultsWriter(object):
    def __init__(self, game):
        self.match = Match.query.filter_by(guid=game).first()

    def valid(self):
        return self.match and not self.match.finished

    def record(self, db, results):
        print "about to write results={}".format(results)
        self.match.finish()
        db.session.add(self.match)
        db.session.commit()
        bots = results.get('bots', [])
        starting_stack = results.get('starting_stack', 0)
        hands = results.get('hands', 1)

        for bot in bots:
            key = bot.get('key', '')
            bot_id = BotIdentity.query.filter_by(key=key).first()
            if not bot_id:
                continue
            stack = bot.get('stack', 0)
            results = MatchResult(self.match, bot_id, hands, stack - starting_stack)
            db.session.add(results)

        db.session.commit()
