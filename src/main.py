"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv('DATABASE_URL')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    character = Character.query.all()
    #print(character)
    return jsonify(list(map(lambda person: person.serialize(), character))), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id = None):
    #print("entre aqui")
    character = Character.query.get(people_id)
    if character is None:
        return jsonify({"message":"Character not found"}), 404
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planet = Planet.query.all()
    return jsonify(list(map(lambda planets: planets.serialize(), planet))), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id = None):
     planet = Planet.query.get(planet_id)
     if planet is None:
        return jsonify({"message":"planet not found"}), 404
     return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    user = User.query.all()
    return jsonify(list(map(lambda users: users.serialize(), user))), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id = None):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message":"user not found"}), 404
    return jsonify(user.serialize()), 200

@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id = None, user_id = None):
    favorite_planet = Planet.query.get(planet_id)
    if favorite_planet is None:
        return jsonify({"message":"planet not found"}), 404
    new_favorite = Favorites(name = favorite_planet.name, nature_id = planet_id, user_id = user_id, nature = 'planets')
    db.session.add(new_favorite)
    try:
        db.session.commit()
        return jsonify(new_favorite.serialize()), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"message":"not found"}), 500
    return jsonify({"message":"internal server error"}), 500

@app.route('/favorite/<int:user_id>/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id = None, user_id = None):
    favorite_character = Character.query.get(people_id)
    if favorite_character is None:
        return jsonify({"message":"planet not found"}), 404
    new_favorite = Favorites(name = favorite_character.name, nature_id = people_id, user_id = user_id, nature = 'character')
    db.session.add(new_favorite)
    try:
        db.session.commit()
        return jsonify(new_favorite.serialize()), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"message":"not found"}), 500
    return jsonify({"message":"internal server error"}), 500

@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorites.query.get(favorite_id)
    if favorite is None:
        return jsonify({"message":"error"})
    db.session.delete(favorite)
    try:
        db.session.commit()
        return jsonify({}), 204
    except Exception as error:
        db.session.rollback()
        return jsonify({"message":"not found"}), 500
    return jsonify({"message":"internal server error"}), 500





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
