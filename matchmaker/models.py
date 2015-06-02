import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from matchmaker import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    registered_on = db.Column('registered_on' , db.DateTime)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.registered_on = datetime.datetime.utcnow()

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
        username = data.get('login', None)
        existing = db.session.query(User).filter_by(username=username).first()
        if existing is not None:
            return existing
        email = data.get('email', None)
        if email is None:
            return None
        user = User(username=username, email=email)
        user.write()
        return user

    def __repr__(self):
        return "User<'{}' {}>".format(self.username, self.email)
