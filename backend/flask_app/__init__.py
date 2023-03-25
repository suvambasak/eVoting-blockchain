from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


database = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['BEGIN'] = not os.path.exists(
        '/home/suvam/Projects/sc5-evoting-g10/backend/instance/db.sqlite'
    )

    database.init_app(app)

    from . import models

    with app.app_context():
        database.create_all()

        if app.config['BEGIN']:
            database.session.add(
                models.Candidate(
                    roll_number='22111007',
                    name='Candidate Name 1'
                )
            )
            database.session.add(
                models.Candidate(
                    roll_number='22111008',
                    name='Candidate Name 2'
                )
            )
            database.session.add(
                models.Candidate(
                    roll_number='22111009',
                    name='Candidate Name 3'
                )
            )
            database.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.Voter.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
