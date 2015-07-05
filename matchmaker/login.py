from flask import redirect, url_for, request, g, Config
from flask_oauthlib.client import OAuth
from flask.ext.login import LoginManager, login_required, login_user, logout_user

from matchmaker import app
from models import User, BotIdentity


# Wire everything up
login_manager = LoginManager()
login_manager.init_app(app)
oauth = OAuth(app)

# Casino GitHub OAuth
oauth_config = Config("")
oauth_config.from_object('matchmaker.default_oauth')
oauth_config.from_envvar('CASINO_OAUTH', silent=True)
github = oauth.remote_app(
    'github',
      **{k.lower(): v for k,v in oauth_config.items()}
)


@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    g.github_token = (resp['access_token'], '')
    # fetch user data via the access token
    me = github.get('user')
    login_user(User.get_or_create(me.data))
    return redirect(url_for('index'))


@github.tokengetter
def get_github_oauth_token():
    return g.get('github_token', None)


@login_manager.user_loader
def load_user_from_session(id):
    return User.query.get(int(id))


@login_manager.request_loader
def load_user_from_bot_key(request):
    """key based authentication for the API"""
    bot_key = request.args.get('key')
    bot = BotIdentity.query.filter_by(key=bot_key).first()
    if bot:
        return bot.get_user()

    return None
