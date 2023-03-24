from flask import Flask
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    database.init_app(app)

    from . import models

    with app.app_context():
        database.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
