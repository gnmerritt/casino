import datetime
from matchmaker import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.Integer, index=True, unique=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    registered_on = db.Column('registered_on' , db.DateTime)

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
        existing = db.session.query(User).filter_by(external_id=external_id).first()
        if existing is not None:
            return existing
        email = data.get('email', None)
        username = data.get('login', None)
        if email is None or username is None:
            return None
        user = User(username=username, email=email, external_id=external_id)
        user.write()
        return user

    def __repr__(self):
        return "User<'{}' {}>".format(self.username, self.email)
