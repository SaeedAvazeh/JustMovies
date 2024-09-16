from flask import request, redirect, url_for, render_template, Blueprint, flash
from flask_login import current_user
import flask_login
from src import model
from datetime import date, timedelta
from app import db 
from functools import wraps
from datetime import datetime
from flask.json import jsonify

bp = Blueprint("manager", __name__)
def manager_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role == model.UserRole.manager:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login', next=request.url))
    return decorated_function

@bp.route("/movie") 
@flask_login.login_required
@manager_only
def movie():
    movies = model.Movie.query.all()
    return render_template("manager_movie.html", movies=movies)


@bp.route("/add_movie")
@flask_login.login_required
@manager_only
def add_movie():
    movies = model.Movie.query.all()
    rooms = model.Room.query.all()
    current_day = date.today().strftime('%Y-%m-%d')
    return render_template("manager_add_movie.html", movies=movies, rooms=rooms, current_day=current_day)


@bp.route("/add_movie", methods=["POST"])
@flask_login.login_required
@manager_only
def add_movie_post():
    room = request.form.get("room")
    title = request.form.get("title")
    image = request.form.get("image")
    day = datetime.strptime(request.form.get("day"), "%Y-%m-%d").date()
    time = datetime.strptime( request.form.get("time") + ':00', "%H:%M:%S").time()
    new_movie = model.Movie(room_id=room, title=title, image=image, day=day, time=time, booked_seat=0)
    db.session.add(new_movie)
    
    try:
        db.session.commit()
        return redirect(url_for("manager.movie"))
    except:
        flash("the Movie can not be added", 'error')
        return redirect(url_for("manager.movie"))


@bp.route("/delete_movie/<int:id>")
@flask_login.login_required
@manager_only
def delete_movie(id):
    current_data = model.Movie.query.get(id)
    db.session.delete(current_data)
    try:
        db.session.commit()
        flash("the Movie is now deleted.", 'success')
        return redirect(url_for("manager.movie"))
    except:
        flash("there is Reservation for this Movie, so it can not be deleted", 'error')
        return redirect(url_for("manager.movie"))


@bp.route("/edit_movie/<int:id>")
@flask_login.login_required
@manager_only
def edit_movie(id):
    current_data = model.Movie.query.filter(model.Movie.id == id).first()
    movies = model.Movie.query.all()
    rooms = model.Room.query.all()
    return render_template("manager_edit_movie.html", movies=movies, rooms=rooms, current_data=current_data)


@bp.route("/edit_movie/<int:id>", methods=["POST"])
@flask_login.login_required
@manager_only
def edit_movie_post(id):
    room = request.form.get("room")
    title = request.form.get("title")
    image = request.form.get("image")
    day = datetime.strptime(request.form.get("day"), "%Y-%m-%d").date()
    time = datetime.strptime(request.form.get("time"), "%H:%M:%S").time()
    movie = model.Movie.query.filter(model.Movie.id == id).first()
    movie.room_id = room
    movie.title = title
    movie.image = image
    movie.day = day
    movie.time = time
    try:
        db.session.commit()
        flash("the Movie is now updated", 'success')
        return redirect(url_for("manager.movie"))
    except:
        flash("the Movie can not be edited", 'error')
        return redirect(url_for("manager.movie"))



@bp.route("/room") 
@flask_login.login_required
@manager_only
def room():
    rooms = model.Room.query.all()
    return render_template("manager_room.html", rooms=rooms)


@bp.route("/add_room")
@flask_login.login_required
@manager_only
def add_room():
    rooms = model.Room.query.all()
    return render_template("manager_add_room.html", rooms=rooms)


@bp.route("/add_room", methods=["POST"])
@flask_login.login_required
@manager_only
def add_room_post():
    name = request.form.get("name")
    total_seats = request.form.get("total_seats")
    type = request.form.get("type")
    seat_price = request.form.get("seat_price")
    new_room = model.Room(name=name, total_seats=total_seats, type=type, seat_price=seat_price)
    db.session.add(new_room)
    try:
        db.session.commit()
        return redirect(url_for("manager.room"))
    except:
        flash("the Room can not be added", 'error')
        return redirect(url_for("manager.room"))


@bp.route("/delete_room/<int:id>")
@flask_login.login_required
@manager_only
def delete_room(id):
    current_data = model.Room.query.get(id)
    db.session.delete(current_data)
    try:
        db.session.commit()
        flash("the Room is now deleted.", 'success')
        return redirect(url_for("manager.room"))
    except:
        flash("the Room can not be deleted", 'error')
        return redirect(url_for("manager.room"))


@bp.route("/edit_room/<int:id>")
@flask_login.login_required
@manager_only
def edit_room(id):
    current_data = model.Room.query.filter(model.Room.id == id).first()
    rooms = model.Room.query.all()
    return render_template("manager_edit_room.html", rooms=rooms, current_data=current_data)


@bp.route("/edit_room/<int:id>", methods=["POST"])
@flask_login.login_required
@manager_only
def edit_room_post(id):
    name = request.form.get("name")
    total_seats = request.form.get("total_seats")
    type = request.form.get("type")
    seat_price = request.form.get("seat_price")
    room = model.Room.query.filter(model.Room.id == id).first()
    room.name = name
    room.total_seats = total_seats
    room.type = type
    room.seat_price = seat_price 
    try:
        db.session.commit()
        flash("the Room is now updated", 'success')
        return redirect(url_for("manager.room"))
    except:
        flash("the Room can not be edited", 'error')
        return redirect(url_for("manager.room"))
