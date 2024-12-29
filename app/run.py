from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app import create_app

app = create_app()
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5001","http://localhost:5001"], "supports_credentials": True}})
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
