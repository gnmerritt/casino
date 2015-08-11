from flask import render_template, send_from_directory, request
from flask.ext.login import login_required, current_user

from matchmaker import app
from profile import PlayerData


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robots.txt')
def static_from_route():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/profile')
@login_required
def profile():
    player = PlayerData(current_user)
    return render_template('profile.html', p=player.data())

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
