from flask import Response, request, abort
from flask.ext.login import login_required

from matchmaker import app, db
import matches
import util


##
## Public API
##

@app.route('/api/matches')
@login_required
def open_matches():
    open = matches.OpenMatches(db)
    return util.paged_json(open.active())

@app.route('/api/matches/all')
@login_required
def all_matches():
    return Response("TODO")


##
## Internal API
##

@app.route('/api/internal/new_game', methods=['POST'])
def new_game():
    return Response("TODO")

@app.route('/api/internal/join/<game_key>', methods=['POST'])
def player_joined(game_key):
    bot_key = request.args.get('key')
    try:
        joiner = matches.MatchJoiner(game_key, bot_key)
        joiner.join(db)
    except Exception as e:
        print "Error joining match: {}".format(e)
        abort(404)
