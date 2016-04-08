import uuid
import datetime

from matchmaker import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.Integer, index=True, unique=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    registered_on = db.Column(db.DateTime)
    max_bots = db.Column(db.Integer)

    def __init__(self, username, email, external_id):
        self.username = username
        self.email = email
        self.registered_on = datetime.datetime.utcnow()
        self.external_id = external_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def write(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_or_create(cls, data):
        external_id = data.get('id', None)
        existing = db.session.query(User) \
            .filter_by(external_id=external_id).first()
        if existing is not None:
            return existing
        email = data.get('email', None)
        username = data.get('login', None)
        if email is None or username is None:
            return None
        app.logger.info("A new user '{}' just joined".format(username))
        user = User(username=username, email=email, external_id=external_id)
        user.max_bots = 1
        user.write()
        return user

    def __repr__(self):
        return "User<'{}' {}>".format(self.username, self.email)


class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def __init__(self, user, balance=0):
        self.user_id = user.id
        self.balance = balance

    def __repr__(self):
        return "BankAccount<{i}=${b}>".format(b=self.balance, i=self.user_id)


class BotIdentity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    guid = db.Column(db.String(36), nullable=False)
    key = db.Column(db.String(36), index=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, user, name):
        self.user_id = user.id
        self.guid = str(uuid.uuid4())
        self.key = str(uuid.uuid4())
        self.name = name

    def __repr__(self):
        return "Bot<'{n}' {i}>".format(i=self.user_id, n=self.name)

    def get_user(self):
        return User.query.get(self.user_id)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), index=True)
    started = db.Column(db.DateTime, nullable=False)
    finished = db.Column(db.DateTime)
    active = db.Column(db.Boolean)

    def __init__(self):
        self.guid = str(uuid.uuid4())
        self.started = datetime.datetime.utcnow()
        self.active = False

    def finish(self):
        self.finished = datetime.datetime.utcnow()
        self.active = False  # just in case

    def players(self):
        return Player.query.filter_by(match=self.id).count()

    def __repr__(self):
        return "Match<id={id}, start={s}, finish={f}, active? {a}>" \
            .format(id=self.id, s=self.started, f=self.finished, a=self.active)


class Player(db.Model):
    """A player is a bot at a poker table"""
    id = db.Column(db.Integer, primary_key=True)
    bot = db.Column(
        db.Integer, db.ForeignKey("bot_identity.id"), nullable=False)
    match = db.Column(db.Integer, db.ForeignKey("match.id"), nullable=False)

    def __init__(self, bot, match):
        self.bot = bot.id
        self.match = match.id


class MatchEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot = db.Column(db.Integer, db.ForeignKey("bot_identity.id"))
    match = db.Column(db.Integer, db.ForeignKey("match.id"))
    timestamp = db.Column(db.DateTime, nullable=False)
    what = db.Column(db.String(50), nullable=False)

    def __init__(self, player, what):
        self.bot = player.bot
        self.match = player.match
        self.timestamp = datetime.datetime.utcnow()
        self.what = what

    def __repr__(self):
        return "Event<{b} did {w} @ {t}>" \
            .format(b=self.bot, w=self.what, t=self.timestamp)


class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match = db.Column(db.Integer, db.ForeignKey("match.id"), nullable=False)
    bot = db.Column(
        db.Integer, db.ForeignKey("bot_identity.id"), nullable=False)
    hands = db.Column(db.Integer, nullable=False)
    delta_chips = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, match, bot, hands, delta_chips):
        self.match = match.id
        self.bot = bot.id
        self.hands = hands
        self.delta_chips = delta_chips
        self.timestamp = datetime.datetime.utcnow()

    def __repr__(self):
        return "MR<b.id={b} d={d} in {h} hands @ {ts}>" \
            .format(d=self.delta_chips, h=self.hands, ts=self.timestamp,
                    b=self.bot)


class BotSkill(db.Model):
    __tablename__ = "bot_skill"
    bot = db.Column(
        db.Integer, db.ForeignKey("bot_identity.id"), nullable=False)
    date = db.Column(db.Date)
    skill = db.Column(db.Integer)
    delta = db.Column(db.Integer)
    games = db.Column(db.Integer)

    primary_key = db.PrimaryKeyConstraint(bot, date)

    def __init__(self, bot, date, skill, old_skill, games):
        self.bot = bot
        self.date = date
        self.skill = skill
        self.delta = skill - old_skill
        self.games = games

    def __repr__(self):
        return "Skill<{b} -> {s} @ {d} in {g}>" \
            .format(d=self.date, b=self.bot, s=self.skill, g=self.games)


class BotRank(db.Model):
    __tablename__ = "bot_rank"
    bot = db.Column(db.Integer, db.ForeignKey("bot_identity.id"),
                    primary_key=True)
    rank = db.Column(db.Integer, nullable=False)

    def __init__(self, bot, rank):
        self.bot = bot
        self.rank = rank

    def __repr__(self):
        return "Rank<{b} ranked #{r}>" \
            .format(b=self.bot, r=self.rank)
