from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complexprogrammer.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avtotest.db'
# app.config['SECRET_KEY'] = '7df06660a1e6b95c9108cdea'
db = SQLAlchemy(app)


from website import views
