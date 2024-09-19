from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError

auth_bp = Blueprint('auth', __name__)

# Define a schema for validation
class UserSchema(Schema):
    username = fields.Str(required=True, validate=lambda x: 3 <= len(x) <= 20)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    role = fields.Str(required=True)

# User Registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate input using marshmallow
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = data['username']
    password = data['password']
    role = data['role']

    # Check if the user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409

    # Create and save the new user
    new_user = User(username=username, password=generate_password_hash(password), role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    username = data['username']
    password = data['password']

    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Create an access token
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()  # Protect the route with JWT
def logout():
    # For JWT, there is usually no logout action needed; just remove the token from the client side.
    return jsonify({'message': 'Logged out successfully'}), 200
