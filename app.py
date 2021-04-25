from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class ArtistModel(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Artist(name= {Name}"

# db.create_all() # Solo una vez

def serialize_artist(artist):
    return  {
                "id": artist.id,
                "name": artist.name,
                "age": artist.age,
                "self": "/artist/" + artist.id
    }

artist_post_args = reqparse.RequestParser()
artist_post_args.add_argument("name", type=str, required=True)
artist_post_args.add_argument("age", type=str, required=True)


resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'age': fields.String,
    'self': fields.String
}

class Artists(Resource):

    @marshal_with(resource_fields)
    def get(self):
        result = ArtistModel.query.all()

        return [serialize_artist(artist) for artist in result]


    @marshal_with(resource_fields)
    def post(self):
        args = artist_post_args.parse_args()
        encoded = b64encode(args['name'].encode()).decode('utf-8')
        result = ArtistModel.query.filter_by(id=encoded).first()
        if result:
            abort(409, message="Artist already exists...")

        artist = ArtistModel(id=encoded, name=args['name'], age=args['age'])
        db.session.add(artist)
        db.session.commit()
        return artist, 201

class Artist(Resource):

    @marshal_with(resource_fields)
    def get(self, artist_id):
        result = ArtistModel.query.filter_by(id=artist_id).first()
        if not result:
            abort(404, message="Could not find artist with that id...")
        
        return serialize_artist(result)
    
    @marshal_with(resource_fields)
    def delete(self, artist_id):
        result = ArtistModel.query.filter_by(id=artist_id).first()
        if not result:
            abort(404, message="Artist doesnt exist...")
        
        db.session.delete(result)
        db.session.commit()

        return '', 204



api.add_resource(Artists, "/artists")
api.add_resource(Artist, "/artists/<string:artist_id>")
# api.add_resource(Video, "/video/<int:video_id>")



if __name__ == "__main__":
    app.run(debug=True) # sacar para production