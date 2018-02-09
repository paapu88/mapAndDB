from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from rest.user import UserRegister
from rest.track import Track, TrackList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'porignvbpaiyhrvb98975sfur8'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Track, '/track/<string:name>')
api.add_resource(TrackList, '/tracks')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
