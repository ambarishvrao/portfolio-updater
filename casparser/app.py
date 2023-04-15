import os
from flask import Flask, flash, redirect, request
from flask import (url_for, current_app as app)
from werkzeug.utils import secure_filename

import casparser

app = Flask(__name__)
UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/parse", methods=['POST'])
def parse_cas():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'])
        file.save(upload_path, filename)
        return casparser.read_cas_pdf(upload_path + filename, "password", output="json")


# favicon
@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='/assets/favicon.ico')
