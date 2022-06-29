from flask import request, Blueprint, jsonify
import json
# from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from sqlalchemy import exc
from soundclaz.extensions import db
from soundclaz.models import Posts, posts_schema, post_schema, Tag, tag_schema, tags_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def home():
    return jsonify({"message": "Everything's okay. contact Joseph John to know how to interact with the API"})


@api.route('/posts')
def get_posts():
    posts = Posts.query.all()
    print(posts)
    # result = tags_schema.dump(posts)
    # print(tags_schema.validate(posts))
    return jsonify(tags_schema.dump(posts))
