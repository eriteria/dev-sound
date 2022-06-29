from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from soundclaz.models import Posts, Tag, Users
from soundclaz.extensions import ckeditor, db

auth = Blueprint('auth', __name__, url_prefix="/auth")


@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(email=request.form.get("email")).first()
        if user is not None:
            if check_password_hash(user.password_hash, request.form.get("password")):
                login_user(user)
                return redirect(request.args.get('next') or url_for('admin.index'))
            else:
                flash('Invalid username or password.')
        else:
            flash("User don\'t exist")

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated():
#         current_user.ping()


@auth.route("/addUser", methods=["POST"])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    new_user = Users(name, email, password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('admin.index'))
