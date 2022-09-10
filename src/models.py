from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class Nature(Enum):
    character = "character",
    planets = "planet",

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    favorites = db.relationship("Favorites", backref = "user", uselist = True)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    #image = db.Column(db.String(250), nullable = False)
    age = db.Column(db.String(5), nullable = False)
    height = db.Column(db.String(5), nullable = False)
    eye_color = db.Column(db.String(50),  nullable=False)
    hair_color = db.Column(db.String(50),  nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return {
        "id": self.id,
        "name": self.name,
        "age": self.age,
        "height": self.height,
        "eye-color": self.eye_color,
        "hair-color": self.hair_color,
        "gender": self.gender,
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable = False)
    #image = db.Column(db.String(250), nullable = False)
    rotation_period = db.Column(db.String(7), nullable = False)
    orbital_period = db.Column(db.String(7), nullable = False)
    gravity = db.Column(db.String(5), nullable = False)
    terrain = db.Column(db.String(150), nullable = False)
    diameter = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
        "id": self.id,
        "name": self.name,
        "rotation_period": self.rotation_period,
        "orbital_period": self.orbital_period,
        "gravity": self.gravity,
        "terrain": self.terrain,
        "diameter": self.diameter,
        "population": self.population,
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nature = db.Column(db.Enum(Nature), nullable=False)
    name = db.Column(db.String(50), nullable = False)
    nature_id = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    
    __table_args__ = (db.UniqueConstraint(
        "user_id",
        "name",
        name = "message_error"
    ),)

    def serialize(self):
        return {
            "id": self.id,
        }
    