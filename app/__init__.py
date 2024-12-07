import json
from datetime import date

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from app.endpoints import endpoints
from app.models.extensions import db
from app.resources.service_user.user_blueprint import user_api
from config import Config


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(endpoints)
    app.register_blueprint(user_api)
    app.json_encoder = CustomJSONEncoder

    with app.app_context():
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        if not database_exists(engine.url):
            create_database(engine.url)
            print("Database created successfully.")
        db.create_all()
        print("Tables created successfully.")

    return app