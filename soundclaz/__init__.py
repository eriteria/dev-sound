from flask import Flask, render_template, Blueprint

from .commands import create_tables, create_tags, create_user, create_blogs, move_to_s3
from .site.routes import site
from .blog.routes import blog
from .api.routes import api
from .auth.routes import auth
from .admin.routes import admin
from .affiliate.routes import affiliate
from .extensions import db, migrate, ma, ckeditor, login_manager, csrf, s3, mail


import logging


logging.basicConfig(filename='record.txt', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')




# def page_not_found(e):
#     return render_template('error_404.html'), 404


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.config['DEBUG'] = True

    # app.register_error_handler(404, page_not_found)
    app.register_blueprint(site)
    app.register_blueprint(blog)
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(affiliate)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db, render_as_batch=True)
        ma.init_app(app)
        ckeditor.init_app(app)
        login_manager.init_app(app)
        csrf.init_app(app)
        s3.init_app(app)
        mail.init_app(app)

    app.cli.add_command(create_tables)
    app.cli.add_command(create_user)
    app.cli.add_command(create_blogs)
    app.cli.add_command(create_tags)
    app.cli.add_command(move_to_s3)
    return app


application = create_app()