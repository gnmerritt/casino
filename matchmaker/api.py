from flask import Response
from flask.ext.login import login_required

from matchmaker import app


@app.route('/api/join')
@login_required
def find_match():
    return Response("find match authenticated")

@app.route('/api/status')
@login_required
def join_match():
    return Response("join_match authenticated")
