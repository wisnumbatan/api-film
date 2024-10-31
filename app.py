# app.py
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from data import movies

app = Flask(__name__)
api = Api(app)

class MovieList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(movies),
            "movies": movies
        }

class MovieDetail(Resource):
    def get(self, movie_id):
        movie = next((m for m in movies if m["id"] == movie_id), None)
        if movie:
            return {
                "error": False,
                "message": "success",
                "movie": movie
            }
        return {"error": True, "message": "Movie not found"}, 404

    def put(self, movie_id):
        data = request.get_json()
        movie = next((m for m in movies if m["id"] == movie_id), None)
        if movie:
            movie.update(data)
            return {
                "error": False,
                "message": "Movie updated successfully",
                "movie": movie
            }
        return {"error": True, "message": "Movie not found"}, 404

    def delete(self, movie_id):
        global movies
        movies = [m for m in movies if m["id"] != movie_id]
        return {
            "error": False,
            "message": "Movie deleted successfully"
        }

class AddMovie(Resource):
    def post(self):
        data = request.get_json()
        new_movie = {
            "id": str(len(movies) + 1),
            "title": data["title"],
            "year": data["year"],
            "genre": data["genre"],
            "director": data["director"],
            "rating": data["rating"]
        }
        movies.append(new_movie)
        return {
            "error": False,
            "message": "Movie added successfully",
            "movie": new_movie
        }, 201

api.add_resource(MovieList, '/movies')
api.add_resource(MovieDetail, '/movies/<string:movie_id>')
api.add_resource(AddMovie, '/movies/add')

if __name__ == '__main__':
    app.run(debug=True)
