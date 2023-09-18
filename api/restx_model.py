# Task 3: Add your solution here
from flask_restx import Api, fields
from api import app

api = Api(app)

movie_model = api.model(
    'Movies',
     {
         'title': fields.String(),
         'genre': fields.String(),
         'release_year': fields.Integer()
     }
 )