from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from app.endpoints import endpoints
from app.models.extensions import db
from app.resources.service_user.user_blueprint import user_api
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.before_request
    def initialize():
        with app.app_context():
            engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

            # Check if the database exists
            if not database_exists(engine.url):
                create_database(engine.url)  # Create the database
                print("Database created successfully.")

            # Create tables based on the models
            db.create_all()
            print("Tables created successfully.")

    app.register_blueprint(endpoints)
    app.register_blueprint(user_api)
    return app