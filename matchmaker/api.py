from flask import request, jsonify
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
    return util.paged_json(open.active(app.config))


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
    joiner = matches.MatchJoiner(game_key, bot_key)
    code, message = joiner.join(db)
    return jsonify(status=code, message=message), code


@app.route('/api/internal/finished/<game_key>', methods=['POST'])
def game_finished(game_key):
    pass
