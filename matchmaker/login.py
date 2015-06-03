from flask import redirect, url_for, request, g
from flask_oauthlib.client import OAuth
from flask.ext.login import LoginManager, login_required, login_user, logout_user

from matchmaker import app
from models import User


# Wire everything up
login_manager = LoginManager()
login_manager.init_app(app)
oauth = OAuth(app)

# Casino-dev
github = oauth.remote_app(
    'github',
    consumer_key='de6135e8b10ffd7eab54',
    consumer_secret='72469afa5f3873ab1b14393d57e4068531334f97',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
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
