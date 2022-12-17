import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bson.objectid import ObjectId
from .database import db

bp = Blueprint('auth', __name__)


@bp.route('auth/register', methods=('GET', 'POST'))
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            if not add_user(username, generate_password_hash(password)):
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template('auth/register.html')


@bp.route("/auth/login", methods=('GET', 'POST'))
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.query("Mitarbeiter", {"username": username})
        print(user)
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['_id']["$oid"]
            return redirect(url_for('admin.admin_overview'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.query("Mitarbeiter", {"_id": ObjectId(user_id)})


@bp.route("/auth/logout")
@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def add_user(username: str, password: str):
    if db.query("Mitarbeiter", {"username": username}):
        return False
    item = {
        "username": username,
        "password": password
    }
    return db.insert_one("Mitarbeiter", item)

