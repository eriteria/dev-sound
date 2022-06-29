import datetime
import os

import click
import json

import flask_s3
from flask.cli import with_appcontext
# from werkzeug.security import generate_password_hash

# from wsgi import app
from .extensions import db
from .models import Users, Posts, Tag, Role


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()


@click.command(name='create_user')
@with_appcontext
def create_user():
    joseph = Users(name="Joseph", email="joseph1@joseph.com", password="7777", role="Administrator")
    maro = Users(name='OdogwuN', email="maro@maro.com", password="maro", role="Moderator")
    db.session.add(maro)
    db.session.add(joseph)
    db.session.commit()


@click.command(name='create_blogs')
@with_appcontext
def create_blogs():
    user = Users.query.filter_by(name="Odogwu Maro")
    content = json.loads(os)
    blog = Posts(user, "The Logo Doesn't Tell The Whole Story", "/static/img/creative-agency/blog/nike.jpg",)
    db.session.add(blog)
    db.session.commit()


@click.command(name="create_tags")
@with_appcontext
def create_tags():
    tag = Tag("Blog Post")
    tag2 = Tag("Inspiration")
    tag3 = Tag("Business")
    Role.insert_roles()
    db.session.add_all([tag, tag2, tag3])
    db.session.commit()


@click.command(name="moveToS3")
@with_appcontext
def move_to_s3():
    # flask_s3.create_all()
    pass