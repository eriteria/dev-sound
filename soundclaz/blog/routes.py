from flask import Blueprint, render_template

from soundclaz.models import Posts, Tag, Permission

blog = Blueprint('blog', __name__, url_prefix="/blog")

# Helper Code

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
ROWS_PER_PAGE = 5


def allowed_file(filename) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blog.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


# Blog Routes
@blog.route("/")
def home():
    # posts = Posts.query.all()
    # tags = Tag.query.all()
    # return render_template("blog/blog.html", posts=posts, tags=tags)
    return render_template("blog/blog.html")



@blog.route("/blog1")
def blog1():
    # posts = Posts.query.all()
    # tags = Tag.query.all()
    # return render_template("blog/blog1.html", posts=posts, tags=tags)
    return render_template("blog/blog1.html")


@blog.route("/blog2")
def blog2():
    # posts = Posts.query.all()
    # tags = Tag.query.all()
    # return render_template("blog/blog2.html", posts=posts, tags=tags)
    return render_template("blog/blog2.html")



@blog.route("/blog3")
def blog3():
    # posts = Posts.query.all()
    # tags = Tag.query.all()
    # return render_template("blog/blog3.html", posts=posts, tags=tags)
    return render_template("blog/blog3.html")


@blog.route("/blog/<int:blog_id>")
def blog_post(blog_id):
    post = Posts.query.get(blog_id)
    all_posts = Posts.query.all()
    return render_template("blog/blog_post.html", post=post, all_posts=all_posts)
