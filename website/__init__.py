from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complexprogrammer.db'
# app.config['SECRET_KEY'] = '7df06660a1e6b95c9108cdea'

api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {"Hello World"}


api.add_resource(HelloWorld, "/HelloWorld")
from website import views
