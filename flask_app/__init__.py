import os
from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
UPLOAD_FOLDER = 'flask_app/static/musica'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_PATH']