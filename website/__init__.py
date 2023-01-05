import os

from flask_socketio import SocketIO

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_session import Session
# from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

TWILIO_ACCOUNT_SID = "AC52dab15eeb8274e7be5c8e08e12ed1c7"
TWILIO_API_KEY_SID = "SK4d94f08b240ca90bbb9e97635f941817"
TWILIO_API_KEY_SECRET = "ClYYGOesl4RYh7oH17tauhSN3iXl3mhg"

UPLOAD_FOLDER = 'C:/Users/odilj/OneDrive/Документы/ImageCompare'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
GET_FILE_FORMATS = {'.mp3', '.mp4', '.zip', '.xml'}
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__)
socketio = SocketIO(app, manage_session=False, async_mode="threading")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 * 1000
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complexprogrammer.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'avtotest_test.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avtotest.db'
# app.config['SECRET_KEY'] = '7df06660a1e6b95c9108cdea'

app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
Session(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


from website import views
