import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

UPLOAD_FOLDER = 'C:/Users/odilj/OneDrive/Документы/ImageCompare'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 * 1000
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complexprogrammer.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'avtotest.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avtotest.db'
# app.config['SECRET_KEY'] = '7df06660a1e6b95c9108cdea'
db = SQLAlchemy(app)
ma = Marshmallow(app)

from website import views
