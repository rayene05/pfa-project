import os
class Config :
    SECRET_KEY= ""
    SQLALCHEMY_DATABASE_URI = "sqlite:///pythonic.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
    FLASK_ADMIN_FLUID_LAYOUT=True
