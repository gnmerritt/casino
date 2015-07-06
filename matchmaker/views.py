from flask import render_template
from flask.ext.login import login_required, current_user

from matchmaker import app
from profile import PlayerData


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    player = PlayerData(current_user)
    return render_template('profile.html', p=player.data())

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
