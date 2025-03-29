# Project Setup

## Pre-requisites
- Python
- MySQL

## Environment Configuration
Set the following environment variables before running the project:

```sh
export ENV=local
export FLASK_ENV=development
export PYTHONPATH=<>
export SQLALCHEMY_DATABASE_URI=mysql+pymysql://<mysql_user>:<mysql_password>@localhost/users_db
export SECRET_KEY=<>
```

Replace placeholders (`<>`) with the appropriate values.

Make sure these are loaded in your current terminal context, by techique like:
```sh
source env_config/local.env
```

## Install dependencies
Ensure that you activate virtual environment & install app dependencies
```sh
pip install -r requirement.txt
```

## Run the app
```sh
python app/run.py
```

##  Create the admin user
The required tables would be auto created on your localhost, when you run the app successfully.

For creating your first admin user, comment out following part from user_blueprint.py
```sh
@user_api.route('/user', methods=['POST'])
-->  @verify_auth_token <--
def create_user(*args, **kwargs):
    data = request.get_json()
```
and
```sh
    if not data or not data.get('username') or not data.get('password') or not data.get('first_name'):
        return jsonify({'message': 'Missing required fields'}), 400

    if not user_data.get("is_admin"):
        return jsonify({'message': 'You have no permissions to create a user'}), 403
```

Create user using follwing api call
```sh
curl --location 'http://127.0.0.1:5000/user' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username":"admin@gmail.com",
  "password":"1234",
  "first_name":"Admin",
  "last_name":"User"
}'
```
 Mark is_admin as true on the database directly. Make sure that uncomment the code after creating the admin user.
 
##  Create other data
Login with admin & get auth token
```sh
curl --location 'http://127.0.0.1:5000/user/login' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username":"admin@gmail.com",
  "password":"1234"
}'
```
Create other users
```sh
curl --location 'http://127.0.0.1:5000/user' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username":"u1@gmail.com",
  "password":"1234",
  "first_name":"User",
  "last_name":"One"
}'
```
List other users
```sh
curl --location 'http://127.0.0.1:5000/user' \
--header 'Authorization: Bearer <token>' \
--data ''
```
Get user by id
```sh
curl --location 'http://127.0.0.1:5000/user/<id>' \
--header 'Authorization: Bearer <token>' \
```