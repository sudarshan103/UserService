from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.service_user_repo import ServiceUserRepo

# Initialize the Blueprint
user_api = Blueprint('user_api', __name__)

@user_api.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password') or not data.get('first_name'):
        return jsonify({'message': 'Missing required fields'}), 400

    new_user = ServiceUserRepo.create(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data.get('last_name')
    )

    return jsonify({"message": "User created successfully", "uuid": new_user.uuid}), 201

@user_api.route('/user', methods=['GET'])
def list_users():
    users = ServiceUserRepo.get_all_users_by_filter(dict(is_deleted=None))
    return jsonify([user.to_dict() for user in users])


@user_api.route('/user/<uuid>', methods=['GET'])
def get_user(uuid):
    user = ServiceUserRepo.get_user_by_filter(dict(uuid=uuid))

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)

@user_api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400

    user = ServiceUserRepo.get_user_by_filter(dict(username=data['username']))

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Create JWT token
    access_token = create_access_token(identity=user.uuid)

    return jsonify({
        'message': 'Login successful',
        'auth_token': access_token,
        'first_name': user.first_name,
        'last_name': user.last_name
    })