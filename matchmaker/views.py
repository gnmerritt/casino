from flask import render_template, send_from_directory, request
from flask.ext.login import login_required, current_user

from matchmaker import app
from profile import PlayerData
from bot_page import BotData
from leaderboard import Leaderboard


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


@app.route('/bot/<bot_id_guid>')
def bot_page(bot_id_guid):
    bot_data = BotData(bot_id_guid)
    return render_template('bot.html', b=bot_data.data())


@app.route('/leaderboard')
def leaderboard():
    leaderboard = Leaderboard(current_user)
    return render_template('leaderboard.html', l=leaderboard.data())
