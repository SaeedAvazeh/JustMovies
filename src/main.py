from datetime import date, datetime, timedelta
import dateutil.tz
from flask import Blueprint, render_template, request, flash, url_for, redirect
import flask_login
from flask_login import current_user
from sqlalchemy import func
from src import model
from app import db

bp = Blueprint("main", __name__)
@bp.route("/")
def index():
    movies = model.Movie.query.all()
    rooms = model.Room.query.all()
    users = model.User.query.all()
    return render_template("main/index.html", movies=movies, rooms=rooms, users=users)


@bp.route("/movie/<int:id>")
def movie(id):
    movies = model.Movie.query.filter.all()
    return render_template("movie.html", movies=movies)


@bp.route("/user")
@flask_login.login_required
def user():
    current_day = date.today()
    now = []
    past = []
    now_reservations = model.Reservation.query.filter(model.Reservation.user_id == current_user.id).order_by(model.Reservation.date_time).all()
    for res in now_reservations:
        if res.movie.day >= current_day:
            now.append(res)
        else:
            past.append(res)
    return render_template('user.html', now_reservations = now, past_reservations = past)


@bp.route("/reservation/", defaults={'id': None})
@bp.route("/reservation/<int:id>")
@flask_login.login_required
def reservation(id):
    current_day = date.today()
    movies = model.Movie.query.filter(model.Movie.day >= current_day).order_by(model.Movie.day.asc(), model.Movie.time.asc()).all()
    if id == None:
        return render_template("reservation.html", movie=None, movies=movies)
    else:
        movie = model.Movie.query.get(id)
        movies = model.Movie.query.filter(model.Movie.id == movie.id, model.Movie.day >= current_day).order_by(model.Movie.day.asc(), model.Movie.time.asc()).all()
        return render_template("reservation.html", movie=movie, movies=movies)


@bp.route("/reservation/", methods=["POST"])
@flask_login.login_required
def reservation_post():
    selected_movie = request.form.get("movie")
    selected_num_seats = request.form.get("seats")
    movie = model.Movie.query.get(selected_movie)
    movie.booked_seat = movie.booked_seat + int(selected_num_seats)
    new_reservation = model.Reservation(user_id=current_user.id, movie_id=movie.id, num_seats=int(selected_num_seats), date_time=datetime.now())
    db.session.add(new_reservation)
    db.session.commit()
    flash("You have bought %s tickets for %s"%(selected_num_seats, movie.title), 'success')
    return redirect(url_for("main.index"))
