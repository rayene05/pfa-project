from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from dev.config import Config
from flask_admin import Admin

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = "users.login1"
login_manager.login_message_category = "info"
admin = Admin(name='VirtualBank', template_mode='bootstrap4')
mail = Mail()
def create_app(config_class=Config):
     app = Flask(__name__)
     app.config.from_object(Config)
     
     
     
     db.init_app(app)
     bcrypt.init_app(app)
     admin.init_app(app)
     login_manager.init_app(app)
     migrate.init_app(app,db)
  
     mail.init_app(app)
     
     from dev.main.routes import main
     from dev.Bankaccounts.routes import bankaccounts_bp
     from dev.Loans.routes import loans
     from dev.Transactions.routes import transactions_bp
     from dev.Users.routes import users
     from dev.errors.handlers import errors
     from dev.adminbp.routes import adminbp
     app.register_blueprint(adminbp)
     app.register_blueprint(main)
     app.register_blueprint(bankaccounts_bp)
     app.register_blueprint(loans)
     app.register_blueprint(transactions_bp)
     app.register_blueprint(users)
     app.register_blueprint(errors)
     
     return app
