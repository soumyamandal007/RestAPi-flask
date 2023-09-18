# Task 1: Add import here

from .models import db

# Task 3: Add import here

from .restx_model import api, movie_model

# Task 5+9: Add your solution here

from flask import  request, jsonify
from flask_restx import  Resource
from .models import Movies
from sqlalchemy.exc import IntegrityError

@api.route('/movies')
class Movie(Resource):
    @api.expect(movie_model, code=200)
    @api.response(409, "Movie already exists")
    @api.response(200, 'Success')
    def post(self):
        ''' Post a new movie '''
        payload = request.get_json()
        title = payload["title"]
        genre = payload["genre"]
        release_year = payload["release_year"]

        new_movie = Movies(title=title, release_year=release_year, genre=genre)
        db.session.add(new_movie)

        try:
            db.session.commit()
            return jsonify(new_movie.to_dict)
        except IntegrityError:
            db.session.rollback()
            api.abort(409, "Movie with the given title already exists")

    @api.response(200, 'Success')
    def get(self):
        ''' Get all movies '''
        movies = Movies.query.all()
        movies = [movie.to_dict for movie in movies]
        return jsonify({"count": len(movies), "movies": movies})
# Task 6+10+11: Add your solution here
@api.route('/movies/<int:id>')
class MovieResource(Resource):
    @api.response(404, 'Movie not Found')
    @api.response(200, 'Success', movie_model)
    def get(self,id):
        ''' Get a movie by ID '''
        movie = Movies.query.get(id)
        if movie:
            return jsonify(movie.to_dict)
        else:
            api.abort(404, message="The movie you are looking for is not found", type="error")

    @api.response(404, 'Movie not Found')
    @api.response(200, 'Success')
    @api.expect(movie_model, code=200)
    def put(self, id):
        ''' Update a movie '''
        movie = Movies.query.get(id)
        if movie:
            payload = request.get_json()
            movie.title = payload["title"]
            movie.genre = payload["genre"]
            movie.release_year = payload["release_year"]
            db.session.commit()
            return jsonify(movie.to_dict)
        else:
            api.abort(404, "The movie you are looking for is not found", type="error")

    @api.response(404, 'Movie not Found')
    @api.response(200, 'Success')
    def delete(self, id):
        ''' Delete a movie'''
        movie_to_be_deleted = Movies.query.get(id)
        if movie_to_be_deleted:
            db.session.delete(movie_to_be_deleted)
            db.session.commit()
            return f'movie with id {id} has been deleted Successfully'
        else:
            api.abort(404, "The movie you are looking for is not found", type="error")


# Task 7: Add your solution here
@api.route('/movies/from_year=<int:start_year>to_year=<int:end_year>')
class MoviesRangeYear(Resource):
    @api.response(200, 'Success')
    def get(self, start_year, end_year):
        ''' Get movies released between a specific year range '''
        movies = Movies.query.filter(Movies.release_year>=start_year, Movies.release_year<=end_year)
        movies = [movie.to_dict for movie in movies]
        return jsonify({"count": len(movies), "movies": movies})
# Task 8: Add your solution here
@api.route('/movies/<string:title>')
class MovieResourceByTitle(Resource):
    @api.response(200, 'Success')
    def get(self, title):
        ''' Get a movie by title'''
        movie = Movies.query.filter(Movies.title==title).first()
        return jsonify(movie.to_dict)