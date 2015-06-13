from flask import Response
from flask.ext.login import login_required

from matchmaker import app, db
import matches
import util


@app.route('/api/matches')
@login_required
def open_matches():
    open = matches.OpenMatches(db)
    return util.paged_json(open.active())

@app.route('/api/matches/all')
@login_required
def all_matches():
    return Response("TODO")
