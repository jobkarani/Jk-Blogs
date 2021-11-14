from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
from flask_simplemde import SimpleMDE

db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
simple = SimpleMDE()
login_manager = LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos', IMAGES)


# creating the application

def create_app(config_name):
    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])
    config_options[config_name].init_app(app)

    # Initializing flask extensions
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    mail.init_app(app)
    simple.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Registering the auth bluprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/user-account')

    # configure UploadSet
    configure_uploads(app, photos)

    return app