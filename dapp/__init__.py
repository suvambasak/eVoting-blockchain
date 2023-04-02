import hashlib
import json
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


def init_candidates(path, db, Candidate):
    import csv

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
            db.session.add(
                Candidate(
                    username=row[0],
                    name=row[1]
                )
            )

        db.session.commit()


def setup_admin(path, db, Users, Election):
    with open(path) as json_file:
        admin_user_details = json.loads(json_file.read())
        db.session.add(
            Users(
                username_hash=hashlib.sha256(
                    bytes(admin_user_details["username"], 'UTF-8')
                ).hexdigest(),
                password=generate_password_hash(
                    admin_user_details["passwd"],
                    method='sha256'
                ),
                wallet_address=admin_user_details["wallet"],
                voter_status=False
            )
        )
        # db.session.commit()

        db.session.add(
            Election(
                contract_address=admin_user_details["contract_address"]
            )
        )

        db.session.commit()


database = SQLAlchemy()


def create_app():
    WORKING_DIRECTORY = os.getcwd()
    DB_NAME = 'offchain.sqlite'
    CSV_DIR = f'{WORKING_DIRECTORY}/CSV/candidates.csv'
    ADMIN_DIR = f'{WORKING_DIRECTORY}/admin/admin.json'

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
            setup_admin(
                ADMIN_DIR,
                database,
                models.Voter,
                models.Election
            )
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

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
