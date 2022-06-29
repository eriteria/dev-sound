import datetime
import hashlib

from flask import current_app, request
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from .extensions import db, ma, login_manager


class Permission:
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    registered_at = db.Column(db.DateTime, default=datetime.datetime.now)
    last_login = db.Column(db.DateTime)
    posts = db.relationship('Posts', backref='users')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    avatar_hash = db.Column(db.String(32))

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password, 'sha256')
        # self.role = role
        if role is None:
            if self.email == current_app.config['SOUNDCLAZ_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            elif self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        else:
            self.role = Role.query.filter_by(name=role).first()

    def __repr__(self):
        return f"Name: {self.name}, Role: {self.role}"

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        if not self.avatar_hash:
            self.avatar_hash = hash
            db.session.commit()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default,
                                                                     rating=rating)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
                )


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    author = db.relationship('Users',
                             backref=db.backref('authored_posts', lazy=True))
    title = db.Column(db.String(100))
    summary = db.Column(db.String(255))
    cover = db.Column(db.String(255))
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())
    published_at = db.Column(db.DateTime)
    content = db.Column(db.Text)
    comments = db.relationship('Comments', backref='comments')
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                           backref=db.backref('posts', lazy=True))

    def __init__(self, author, title, cover, content, post_tags):
        self.author = author
        self.title = title
        self.content = content
        self.cover = cover
        self.tags.append(Tag.query.filter_by(name=post_tags).first())


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_post = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'))
    title = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    content = db.Column(db.String(1024))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))

    def __init__(self, name):
        self.name = name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('Users', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


# Marshmallow Schema
class PostsSchema(ma.Schema):
    class Meta:
        model = Posts
        field = ('id', 'title')


class TagSchema(ma.Schema):
    class Meta:
        model = Posts
        fields = ('id', 'title', 'tags', 'content')


# Init Schema
post_schema = PostsSchema()
posts_schema = PostsSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
