from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complexprogrammer.db'
# app.config['SECRET_KEY'] = '7df06660a1e6b95c9108cdea'






from website import views
