from flask import Blueprint, render_template, request, redirect, url_for, flash
import flask_login
from app import db, bcrypt
from src import model

bp = Blueprint("auth", __name__)
@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")


@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")
    
    if role == 'manager':
        role = model.UserRole.manager
    else:
        role = model.UserRole.customer
    if password != request.form.get("password_repeat"):
        flash("Passwords are different. Try again please.", 'error')
        return redirect(url_for("auth.signup"))
    user = model.User.query.filter_by(email=email).first()
    if user:
        flash("You are already Signed up!", 'error')
        return redirect(url_for("auth.signup"))
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = model.User(email=email, name=username, password=password_hash, role=role)
    db.session.add(new_user)
    db.session.commit()
    flash("You are now signed up!", 'success')
    return redirect(url_for("auth.login"))


@bp.route("/login")
def login():
    return render_template("auth/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    user = model.User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        flask_login.login_user(user)
        flash("You are now Signed in!", 'success')
        return redirect(url_for("main.index"))
    else:
        if user == None:
            flash("You need to Sign up first!", 'error')
            return redirect(url_for("auth.login"))
        if user.email == email and bcrypt.check_password_hash(user.password, password) == 0:
            flash("Wrong password, try again please.", 'error')
        return redirect(url_for("auth.login"))

@bp.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flash ('You are now Signed out', 'success')
    return redirect(url_for("auth.login"))