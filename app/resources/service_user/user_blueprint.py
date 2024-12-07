import json

from flask import Blueprint, request, jsonify

from app.models.extensions import ApiJSONEncoder
from app.models.service_user_repo import ServiceUserRepo
from app.resources.core.auth import verify_auth_token, generate_token

# Initialize the Blueprint
user_api = Blueprint('user_api', __name__)

@user_api.route('/user', methods=['POST'])
@verify_auth_token
def create_user(*args, **kwargs):
    data = request.get_json()
    user_data = kwargs.get("user_data")
    if not data or not data.get('username') or not data.get('password') or not data.get('first_name'):
        return jsonify({'message': 'Missing required fields'}), 400

    if not user_data.get("is_admin"):
        return jsonify({'message': 'You have no permissions to create a user'}), 403

    new_user = ServiceUserRepo.create(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data.get('last_name'),
        password=data.get('password')
    )

    return jsonify({"message": "User created successfully", "uuid": new_user.uuid}), 201

@user_api.route('/user', methods=['GET'])
@verify_auth_token
def list_users(**kwargs):
    users = ServiceUserRepo.get_all_users_by_filter(dict(deleted_at=None))
    return json.dumps([user._asdict() for user in users], cls=ApiJSONEncoder)


@user_api.route('/user/<uuid>', methods=['GET'])
@verify_auth_token
def get_user(**kwargs):
    user = ServiceUserRepo.get_user_by_filter(dict(uuid=kwargs.get("uuid")))

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return json.dumps(user._asdict(), cls=ApiJSONEncoder)


@user_api.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400

    user = ServiceUserRepo.authenticate_user(dict(username=data['username']))

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Create JWT token
    access_token = generate_token(user_id=user.id,additional_data= {"is_admin":user.is_admin})

    return jsonify({
        'message': 'Login successful',
        'auth_token': access_token,
        'first_name': user.first_name,
        'last_name': user.last_name
    })