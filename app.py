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
    artist_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    times_played = db.Column(db.Integer, nullable=False)

# db.create_all() # Solo una vez

def serialize_artist(artist):
    base = "https://t2-tgomez.herokuapp.com/"
    return  {
                "id": artist.id,
                "name": artist.name,
                "age": artist.age,
                "albums": base + "artists/" + artist.id + "/albums", 
                "tracks": base  + "artists/" + artist.id + "/tracks",
                "self": base + "artists/" + artist.id
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
                "artist": base + "artists/" + track.artist_id,
                "album": base + "albums/" + track.album_id,
                "self": base + "tracks/" + track.id
    }

artist_post_args = reqparse.RequestParser()
artist_post_args.add_argument("name", type=str, required=True)
artist_post_args.add_argument("age", type=str, required=True)

album_post_args = reqparse.RequestParser()
album_post_args.add_argument("name", type=str, required=True)
album_post_args.add_argument("genre", type=str, required=True)

track_post_args = reqparse.RequestParser()
track_post_args.add_argument("name", type=str, required=True)
track_post_args.add_argument("duration", type=int, required=True)

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
        encoded_id = b64encode(args['name'].encode()).decode('utf-8')
        if len(encoded_id) > 22:
            encoded_id = encoded_id[0:22]

        result = ArtistModel.query.filter_by(id=encoded_id).first()
        if result:
            abort(409, message="Artista ya existe")

        artist = ArtistModel(id=encoded_id, name=args['name'], age=args['age'])
        db.session.add(artist)
        db.session.commit()
        return serialize_artist(artist), 201

class Artist(Resource):

    @marshal_with(artist_fields)
    def get(self, artist_id):
        print("obtener un artista")
        result = ArtistModel.query.filter_by(id=artist_id).first()
        if not result:
            abort(404, message="Could not find artist with that id...")
        
        return serialize_artist(result)
    
    # FALTA ELIMINAR LOS ALBUMS Y CANCIONES
    @marshal_with(artist_fields)
    def delete(self, artist_id):
        print("borrar un artista")
        result = ArtistModel.query.filter_by(id=artist_id).first()
        if not result:
            abort(404, message="artista inexistente")
        
        albums = AlbumModel.query.filter_by(artist_id=artist_id).all()

        for album in albums:
            db.session.delete(album)

        tracks = TrackModel.query.filter_by(artist_id=artist_id).all()

        for track in tracks:
            db.session.delete(track)

        db.session.delete(result)
        db.session.commit()

        return '', 204

class all_albums(Resource):

    @marshal_with(album_fields)
    def get(self):
        print("get all albums")
        result = AlbumModel.query.all()
        return [serialize_album(album) for album in result]

class Album(Resource):

    @marshal_with(album_fields)
    def get(self, album_id):
        print("obtener un album")
        result = AlbumModel.query.filter_by(id=album_id).first()
        if not result:
            abort(404, message="album no encontado")
        
        return serialize_album(result), 200
    
    # FALTA ELIMINAR TODAS LAS CANCIONES
    @marshal_with(album_fields)
    def delete(self, album_id):
        print("borrar un album y todas sus canciones")
        result = AlbumModel.query.filter_by(id=album_id).first()
        if not result:
            abort(404, message="album inexistente")
        
        tracks = TrackModel.query.filter_by(album_id=album_id).all()

        for track in tracks:
            db.session.delete(track)

        db.session.delete(result)
        db.session.commit()

        return 'album eliminado', 204

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
        if len(encoded_id) > 22:
            encoded_id = encoded_id[0:22]
        # ARREGLAR, dos artistas pueden tener un album con el mismo nombre
        find_album = AlbumModel.query.filter_by(id=encoded_id).first() 
        if find_album:
            abort(409, message="album ya existe") # Debe retornar el album

        find_artist = ArtistModel.query.filter_by(id=artistId).first()
        if not find_artist:
            abort(422, message="artista no existe")

        album = AlbumModel(id=encoded_id, artist_id=artistId, name=args['name'], genre=args['genre'])

        db.session.add(album)
        db.session.commit()
        return serialize_album(album), 201

class artist_tracks(Resource):

    @marshal_with(track_fields)
    def get(self, artistId):
        print("get tracks from artist")
        artist = ArtistModel.query.filter_by(id=artistId).first()
        if not artist:
            abort(404, message="artista no encontrado")

        tracks = TrackModel.query.filter_by(artist_id=artistId).all()

        return [serialize_track(track) for track in tracks]

class all_tracks(Resource):

    @marshal_with(track_fields)
    def get(self):
        print("get all tracks")
        result = TrackModel.query.all()
        return [serialize_track(track) for track in result]

class Track(Resource):

    @marshal_with(track_fields)
    def get(self, track_id):
        print("obtener un track")
        result = TrackModel.query.filter_by(id=track_id).first()
        if not result:
            abort(404, message="album no encontado")
        
        return serialize_track(result), 200
    
    @marshal_with(track_fields)
    def delete(self, track_id):
        print("borrar un track")
        result = TrackModel.query.filter_by(id=track_id).first()
        if not result:
            abort(404, message="album inexistente")
        
        db.session.delete(result)
        db.session.commit()

        return 'album eliminado', 204

class album_track(Resource):

    @marshal_with(track_fields)
    def get(self, albumId):
        print("get tracks from album")
        result = TrackModel.query.filter_by(album_id=albumId).all()
        if not result:
            abort(404, message="Album inexistente")

        return [serialize_track(track) for track in result]
    
    @marshal_with(track_fields)
    def post(self, albumId):
        args = track_post_args.parse_args()
        to_encode = args['name'] + ":" + albumId
        encoded_id = b64encode(to_encode.encode()).decode('utf-8')
        if len(encoded_id) > 22:
            encoded_id = encoded_id[0:22]
        find_album = AlbumModel.query.filter_by(id=albumId).first()
        if not find_album:
            abort(422, message="album no existe")
        #FAlta el manejo de errores

        track = TrackModel(id=encoded_id, album_id=albumId, artist_id= find_album.artist_id ,name=args['name'], duration=args['duration'], times_played=0)
        db.session.add(track)
        db.session.commit()
        return serialize_track(track), 201

class play_track(Resource):
    
    def put(self, track_id):
        track = TrackModel.query.filter_by(id=track_id).first()
        if not track:
            abort(404, message="cancion no encontrada")

        track.times_played = track.times_played + 1

        db.session.commit()

        return  'cancion reproducida', 200

class play_album(Resource):

    def put(self, albumId):
        album = AlbumModel.query.filter_by(id=albumId).first()
        
        if not album:
            abort(404, message="album no encontrado")

        tracks = TrackModel.query.filter_by(album_id=albumId).all()

        for track in tracks:
            track.times_played = track.times_played + 1

        db.session.commit()

        return 'canciones del album reproducidas', 200

class play_artist(Resource):

    def put(self, artistId):
        artist = ArtistModel.query.filter_by(id=artistId).first()
        if not artist:
            abort(404, message="artista no encontrado")
        
        tracks = TrackModel.query.filter_by(artist_id=artistId).all()

        for track in tracks:
            track.times_played = track.times_played + 1

        db.session.commit()

        return 'Todas las canciones del artista fueron reproducidas', 200

api.add_resource(Artists, "/artists")
api.add_resource(Artist, "/artists/<string:artist_id>")
api.add_resource(all_albums, "/albums")
api.add_resource(Album, "/albums/<string:album_id>")
api.add_resource(artist_album, "/artists/<string:artistId>/albums")
api.add_resource(artist_tracks, "/artists/<string:artistId>/tracks")
api.add_resource(all_tracks, "/tracks")
api.add_resource(Track, "/tracks/<string:track_id>")
api.add_resource(album_track, "/albums/<string:albumId>/tracks")

# Play
api.add_resource(play_track, "/tracks/<string:track_id>/play")
api.add_resource(play_album, "/albums/<string:albumId>/tracks/play")
api.add_resource(play_artist, "/artists/<string:artistId>/albums/play")



if __name__ == "__main__":
    app.run() # sacar para production