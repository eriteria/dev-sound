from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_s3 import FlaskS3
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
ckeditor = CKEditor()
login_manager = LoginManager()
csrf = CSRFProtect()
s3 = FlaskS3()
mail = Mail()