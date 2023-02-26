import os
from flask import Flask
from flask_socketio import SocketIO

# from flask_session import Session

UPLOAD_FOLDER = 'C:/Users/odilj/OneDrive/Документы/ImageCompare'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
GET_FILE_FORMATS = {'.mp3', '.mp4', '.zip', '.xml'}
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
mode = "dev"
app = Flask(__name__)
socketio = SocketIO(app, manage_session=False, async_mode="threading")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 * 1000
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complexprogrammer.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'avtotest_test.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avtotest.db'
app.config['SECRET_KEY'] = '7df06660a1e6b95c9108cdea'

app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
# Session(app)


# @app.route("/")
# def hello():
#     return "Hello, World!"


# from website import models
from website import views
