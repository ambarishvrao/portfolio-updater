import os
from flask import Flask
from flask import (url_for, current_app as app)
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"


# favicon
@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='/assets/favicon.ico')