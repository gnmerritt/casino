from flask import request, abort, jsonify
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


##
## Internal API
##

@app.route('/api/internal/new_match', methods=['POST'])
def new_match():
    maker = matches.NewMatch()
    maker.create(db)
    return jsonify(**{
        "key": maker.guid(),
        "success": True,
    })

@app.route('/api/internal/join/<game_key>', methods=['POST'])
def player_joined(game_key):
    bot_key = request.args.get('key')
    try:
        joiner = matches.MatchJoiner(game_key, bot_key)
        joiner.join(db)
    except Exception as e:
        print "Error joining match: {}".format(e)
        abort(404)
