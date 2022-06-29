import os
from datetime import timedelta

FLASK_DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/joseph/PycharmProjects/soundclaz/soundclaz/db.sqlite3'
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')

SQLALCHEMY_TRACK_MODIFICATIONS = False
# SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'fhdgjhdfkc ,yrikrykn'
USE_SESSION_FOR_NEXT = True
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
# UPLOAD_FOLDER = f"{S3_LOCATION}static/content"
UPLOAD_FOLDER = "/static/content"
CKEDITOR_PKG_TYPE = 'full'
CKEDITOR_FILE_UPLOADER = 'admin.upload'
SOUNDCLAZ_ADMIN = "joseph1@joseph.com"
CKEDITOR_UPLOAD_ERROR_MESSAGE = "Uploaded not!!"
CKEDITOR_EXTRA_PLUGINS = ['']
CKEDITOR_ENABLE_CSRF = True
FLASKS3_BUCKET_NAME = 'accoms'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
MAIL_SERVER = 'mail.privateemail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'support@soundclaz.com'
MAIL_PASSWORD = 'support2020soundclaz'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_SUPPRESS_SEND = False

# MAX_CONTENT_LENGTH = 5 * 1024 * 1024
# UPLOAD_EXTENSIONS = ['.pdf', '.doc', '.docx']
# UPLOADED_FILES_DEST = 'uploads'
# # USER_LOGIN_URL = '/admin/login'
# USER_SEND_PASSWORD_CHANGED_EMAIL = False
# USER_SEND_USERNAME_CHANGED_EMAIL = False
# USER_SEND_REGISTERED_EMAIL = False
