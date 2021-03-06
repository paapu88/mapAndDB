import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from rest.user import UserRegister
from rest.track import Track, TrackList

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'porignvbpaiyhrvb98975sfur8'
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

#comment this in heroku BEGIN
#@app.before_first_request
#def create_tables():
#    db.create_all()
#comment this in heroku END

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Track, '/track/<string:name>')
api.add_resource(TrackList, '/tracks')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
