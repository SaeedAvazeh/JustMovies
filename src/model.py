from flask import json
from app import db
import flask_login
import enum

class UserRole(enum.Enum):
    guest = 0
    customer = 1
    manager = 2

class User(flask_login.UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), unique=False, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    role = db.Column(db.Enum(UserRole), unique=False, nullable=False)
    user_reservations = db.relationship('Reservation', backref='user', lazy=True)
    
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    title = db.Column(db.String(240), unique=False, nullable=False)
    image = db.Column(db.String(2024))
    day = db.Column(db.Date(), unique=False, nullable=False)
    time = db.Column(db.Time(), unique=False, nullable=False)
    booked_seat = db.Column(db.Integer, unique=False, nullable=False)
    movie_reservations = db.relationship('Reservation', backref='movie', lazy=True)

class Room(db.Model):
    __tablename__ = "room"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    total_seats = db.Column(db.Integer, unique=False, nullable=False)
    type = db.Column(db.String(60), unique=False, nullable=False)
    seat_price = db.Column(db.Integer, unique=False, nullable=False)
    room_movie = db.relationship('Movie', backref='room', lazy=True)

class Reservation(db.Model):
    __tablename__ = "reservation"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    num_seats = db.Column(db.Integer, unique=False, nullable=False)
    date_time = db.Column(db.DateTime(), unique=False, nullable=False)
