from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.track import TrackModel

class Track(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date',
        #defaults to string
        required=True,
        help="This field cannot be left blank!"
    )

    #@jwt_required()
    def get(self, name):
        track = TrackModel.find_by_name(name)
        if track:
            return track.json()
        return {'message': 'Track not found'}, 404

    def post(self, name):
        if TrackModel.find_by_name(name):
            return {'message': "An track '{}' is already there.".format(name)}, 400

        data = Track.parser.parse_args()

        track = TrackModel(name, data['date'])

        try:
            track.save_to_db()
        except:
            return {"message": "An error occurred when adding track to DB."}, 500

        return track.json(), 201

    def delete(self, name):
        track = TrackModel.find_by_name(name)
        if track:
            track.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Track.parser.parse_args()

        track = TrackModel.find_by_name(name)

        if track:
            track.date = data['date']
        else:
            track = TrackModel(name, data['date'])

        track.save_to_db()

        return track.json()

class TrackList(Resource):
    def get(self):
        return {'tracks': list(map(lambda x: x.json(), TrackModel.query.all()))}
