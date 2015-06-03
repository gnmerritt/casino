from flask import Response
from flask.ext.login import login_required

from matchmaker import app


@app.route('/')
def index():
    return Response("Hello index")

@app.route('/profile')
@login_required
def profile():
    return Response("Hello profile")
