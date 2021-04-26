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

class AlbumModel(db.Model):
    id = db.Column(db.String, primary_key=True)
    artist_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)

class TrackModel(db.Model):
    id = db.Column(db.String, primary_key=True)
    album_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    times_played = db.Column(db.Integer, nullable=False)

# db.create_all() # Solo una vez

def serialize_artist(artist):
    base = "https://t2-tgomez.herokuapp.com/"
    return  {
                "id": artist.id,
                "name": artist.name,
                "age": artist.age,
                "albums": base + artist.id + "/albums", 
                "tracks": base  + artist.id + "/tracks",
                "self": base + "artist/" + artist.id
    }

def serialize_album(album):
    base = "https://t2-tgomez.herokuapp.com/"
    return {
                "id": album.id,
                "artist_id": album.artist_id,
                "name": album.name,
                "genre": album.genre,
                "artist": base + "artists/" + album.artist_id,
                "tracks": base + "albums/" + album.id + "/tracks",
                "self": base + "albums/" + album.artist_id
    }

def serialize_track(track):
    base = "https://t2-tgomez.herokuapp.com/"
    return {
                "id": track.id,
                "name": track.name,
                "duration": track.duration,
                "times_played": track.times_played,
                "artist": "Falta solucionar",
                "album": base + "albums/" + track.album_id,
                "self": base + "tracks/" + track.id
    }

artist_post_args = reqparse.RequestParser()
artist_post_args.add_argument("name", type=str, required=True)
artist_post_args.add_argument("age", type=str, required=True)

album_post_args = reqparse.RequestParser()
album_post_args.add_argument("name", type=str, required=True)
album_post_args.add_argument("genre", type=str, required=True)

artist_fields = {
    'id': fields.String,
    'name': fields.String,
    'age': fields.String,
    'albums': fields.String,
    'tracks': fields.String,
    'self': fields.String
}

album_fields = {
    'id': fields.String,
    'artist_id': fields.String,
    'name': fields.String,
    'genre': fields.String,
    'artist': fields.String,
    'tracks': fields.String,
    'self': fields.String
}

track_fields = {
    'id': fields.String,
    'name': fields.String,
    'duration': fields.Integer,
    'times_played': fields.Integer,
    'artist': fields.String,
    'album': fields.String,
    'self': fields.String
}

class Artists(Resource):

    @marshal_with(artist_fields)
    def get(self):
        result = ArtistModel.query.all()
        return [serialize_artist(artist) for artist in result]


    @marshal_with(artist_fields)
    def post(self):
        args = artist_post_args.parse_args()
        encoded = b64encode(args['name'].encode()).decode('utf-8')
        result = ArtistModel.query.filter_by(id=encoded).first()
        if result:
            abort(409, message="Artist already exists...")

        artist = ArtistModel(id=encoded, name=args['name'], age=args['age'])
        db.session.add(artist)
        db.session.commit()
        return serialize_artist(artist), 201

class Artist(Resource):

    @marshal_with(artist_fields)
    def get(self, artist_id):
        result = ArtistModel.query.filter_by(id=artist_id).first()
        if not result:
            abort(404, message="Could not find artist with that id...")
        
        return serialize_artist(result)
    
    '''@marshal_with(resource_fields)
    def delete(self, artist_id):
        result = ArtistModel.query.filter_by(id=artist_id).first()
        if not result:
            abort(404, message="Artist doesnt exist...")
        
        ArtistModel.query.filter_by(id=artist_id).delete()
        #db.session.delete(result)
        #db.session.commit()

        return '', 204'''

class all_albums(Resource):

    @marshal_with(album_fields)
    def get(self):
        print("get all albums")
        result = AlbumModel.query.all()
        return [serialize_album(album) for album in result]

class artist_album(Resource):
    
    @marshal_with(album_fields)
    def get(self, artistId):
        print("get albums from artist")
        result = AlbumModel.query.filter_by(artist_id=artistId).all()
        if not result:
            abort(404, message="Could not find artist with that id...")

        return [serialize_album(album) for album in result]

    @marshal_with(album_fields)
    def post(self, artistId):
        args = album_post_args.parse_args()
        to_encode = args['name'] + ":" + artistId
        encoded_id = b64encode(to_encode.encode()).decode('utf-8')
        # ARREGLAR, dos artistas pueden tener un album con el mismo nombre
        result = AlbumModel.query.filter_by(id=encoded_id).first() 
        if result:
            abort(409, message="album ya existe") # Debe retornar el album


        album = AlbumModel(id=encoded_id, artist_id=artistId, name=args['name'], genre=args['genre'])

        db.session.add(album)
        db.session.commit()
        return serialize_album(album), 201

class all_tracks(Resource):

    @marshal_with(track_fields)
    def get(self):
        print("get all tracks")
        result = TrackModel.query.all()
        return [serialize_track(track) for track in result]





api.add_resource(Artists, "/artists")
api.add_resource(Artist, "/artists/<string:artist_id>")
api.add_resource(all_albums, "/albums")
api.add_resource(artist_album, "/artists/<string:artistId>/albums")
api.add_resource(all_tracks, "/tracks")



if __name__ == "__main__":
    app.run(debug=True) # sacar para production