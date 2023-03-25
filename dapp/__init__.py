import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


def init_candidates(path, db, Candidate):
    import csv

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
            db.session.add(
                Candidate(
                    roll_number=row[0],
                    name=row[1]
                )
            )

        db.session.commit()


database = SQLAlchemy()


def create_app():
    WORKING_DIRECTORY = os.getcwd()
    DB_NAME = 'offchain.sqlite'
    CSV_DIR = f'{WORKING_DIRECTORY}/CSV/candidates.csv'

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['EPOCH'] = not os.path.exists(
        f'{WORKING_DIRECTORY}/instance/offchain.sqlite'
    )

    database.init_app(app)

    from . import models
    with app.app_context():
        database.create_all()

        if app.config['EPOCH']:
            init_candidates(
                CSV_DIR,
                database,
                models.Candidate,
            )

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
