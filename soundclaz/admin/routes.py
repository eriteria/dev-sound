import datetime
import json
import os
import random
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app, jsonify, \
    make_response, flash
from flask_ckeditor import upload_success, upload_fail
from flask_login import login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from soundclaz.models import Posts, Tag, Users, Permission, Role
from soundclaz.settings import UPLOAD_FOLDER
from soundclaz.extensions import ckeditor, db
from soundclaz.decorators import admin_required, permission_required

admin = Blueprint('admin', __name__, url_prefix="/admin")

# Helper Code

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
ROWS_PER_PAGE = 5


def allowed_file(filename) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@login_required
@admin.route("/posts", methods=["POST", "GET"])
def posts():
    page = request.args.get('page', 1, type=int)
    search = request.form.get('search')
    if request.method == 'POST':
        return redirect(url_for('admin.search_results', search=search))
    posts = Posts.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template("admin/posts.html", posts=posts)


@login_required
@admin.route('/results/<search>')
def search_results(search):
    results = []
    # search_string = search.data['search']
    page = request.args.get('page', 1, type=int)

    if search == '':
        posts = db.session.query(Posts).paginate(page=page, per_page=ROWS_PER_PAGE)

    if not results:
        flash('No results found!')
        return render_template('admin/posts.html')
    else:
        # display results
        return render_template('admin/posts.html', posts=posts)


@admin.route('/categories')
@login_required
def categories():
    categories = Tag.query.all()
    return render_template("admin/categories.html", categories=categories)


@admin.route("/")
@login_required
def index():
    latest_posts = Posts.query.order_by('created_at')
    no_of_posts = len(Posts.query.all())
    no_of_tags = len(Tag.query.all())
    no_of_users = len(Users.query.all())
    roles = Role.query.all()
    return render_template("admin/index.html", latest_posts=latest_posts, no_of_posts=no_of_posts,
                           no_of_tags=no_of_tags, tags=Tag.query.all(), no_of_users=no_of_users, roles=roles)


@admin.route("/UpdatePosts", methods=["POST"])
@login_required
def update_post():
    post = Posts.query.get()
    if post:
        pass
    else:
        pass
    return redirect(url_for('admin.new_post'))


@admin.route("/details/<post_id>")
@login_required
def details(post_id):
    post = Posts.query.get(post_id)
    tags = Tag.query.all()
    return render_template("admin/details.html", post=post, tags=tags)


@admin.route("/addPost", methods=["POST"])
@login_required
def add_post():
    imgURL = ""
    title = request.form.get('title')
    tag = request.form.get('tag')
    body = request.form.get('ckeditor')
    file = request.files["image"]
    if file.filename == '':
        flash("No file was uploaded")
    if file and allowed_file(file.filename):
        if os.path.exists(UPLOAD_FOLDER + "/" + file.filename):  # if image with same name exists
            _dot = file.filename.find(".")
            file.filename = file.filename[:_dot] + str(uuid.uuid4()) + file.filename[_dot:]
        filename = secure_filename(file.filename)
        file.save(os.path.normpath(os.path.join(UPLOAD_FOLDER, filename)))
        imgURL = url_for('static', filename=f"content/{filename}")
    post = Posts(current_user, title, imgURL, body, tag)
    # post.id = 80
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('admin.index'))


@admin.route("/deletePost", methods=["POST"])
@login_required
def delete_post():
    post_id = int(json.loads(request.data)['postId'])
    post = Posts.query.filter_by(id=post_id)
    if post:
        post.delete()
        db.session.commit()
    return jsonify({"url": f'{url_for("admin.posts")}'})


@admin.route("/editPost/<int:post_id>", methods=["POST"])
@login_required
def edit_post(post_id):
    post = Posts.query.get(post_id)
    imgURL = ""
    post.title = request.form.get('edit_title')
    post.tag = request.form.get('edit_category')
    post.body = request.form.get('ckeditor')
    file = request.files["image"]
    if file.filename == '':
        flash("No file was uploaded")
    if file and allowed_file(file.filename):
        if os.path.exists(UPLOAD_FOLDER + "/" + file.filename):  # if image with same name exists
            _dot = file.filename.find(".")
            file.filename = file.filename[:_dot] + str(uuid.uuid4()) + file.filename[_dot:]
        filename = secure_filename(file.filename)
        file.save(os.path.normpath(os.path.join(UPLOAD_FOLDER, filename)))
        post.cover = url_for('static', filename=f"content/{filename}")
    db.session.commit()
    return redirect(url_for('admin.index'))


@admin.route('/files/<path:filename>')
@login_required
def uploaded_files(filename):
    path = UPLOAD_FOLDER
    return send_from_directory(path, filename)


@admin.route('/upload', methods=['POST'])
@login_required
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    url = url_for('admin.uploaded_files', filename=f.filename)
    return upload_success(url=url)  # return upload_success call


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@admin.route('/addCategory', methods=['POST'])
@login_required
def add_tag():
    tag = request.form.get('categoryName')
    new_tag = Tag(tag)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(url_for('admin.index'))


@admin.route('/users')
@login_required
def users():
    # users = Users.query.all()
    page = request.args.get('page', 1, type=int)
    users = Users.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('admin/users.html', users=users)


@admin.route('/user/<int:id>')
@login_required
def user_details(id):
    user = Users.query.get(id)
    roles = Role.query.all()
    return render_template('admin/user_details.html', user=user, roles=roles)


@admin.route('/updateProfile/<int:id>', methods=["POST"])
@login_required
def update_profile(id):
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')
    password = request.form.get('password')
    user = Users.query.get(id)
    if user.name != name:
        user.name = name
    if user.email != email:
        user.email = email
    if user.role != role:
        if role != "None":
            role = Role.query.filter_by(name=role).first()
            user.role = role
        else:
            role = Role.query.filter_by(default=True).first()
            user.role = role
    if password:
        user.password = generate_password_hash(password, "sha256")
    db.session.commit()
    return redirect(url_for('admin.user_details', id=id))


@admin.route("/deleteUser", methods=["POST", "GET"])
@login_required
def delete_user():
    user_id = int(json.loads(request.data)['userId'])
    if user_id == current_user.id:
        logout_user()
        Users.query.filter_by(id=user_id).delete()
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        Users.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for("admin.users"))


@admin.route("/profile")
@login_required
def profile():
    return render_template("admin/profile.html")
