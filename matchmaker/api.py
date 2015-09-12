from flask import request, jsonify, abort
from flask.ext.login import login_required, current_user

import bots
from matchmaker import app, db
import matches
import util
import profile


#
#  Public API
#

@app.route('/api/matches')
@login_required
def open_matches():
    open = matches.OpenMatches(db)
    return util.paged_json(open.active(app.config))


@app.route('/api/bot/<guid_or_key>')
def get_bot(guid_or_key):
    bot = bots.BotInfo(db, guid_or_key).bot
    if not bot:
        abort(404)
    return jsonify({
        "success": True,
        "bot": bot,
    })


@app.route('/api/bot/<name>', methods=['POST'])
@login_required
def new_bot(name):
    creator = profile.BotMaker(current_user, name)
    bot = creator.create(db)
    return jsonify({
        "success": True,
        "bot": bot,
    })

#
# Internal API
#


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
    match_results = request.get_json(force=True)
    if not match_results:
        abort(404)
    writer = matches.MatchResultsWriter(game_key)
    if not writer.valid():
        abort(404)
    writer.record(db, match_results)
    new_match = matches.MatchCreatorJob(db)
    new_match.run()
    return jsonify({"success": True})
