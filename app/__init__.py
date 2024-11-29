from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.resources.service_user.user_blueprint import user_api
from config import Config
from app.endpoints import endpoints
from flask_jwt_extended import JWTManager

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
app.register_blueprint(endpoints)
app.register_blueprint(user_api)
db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)
