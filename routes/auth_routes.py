from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import db
from models import User

auth_routes = Blueprint('auth_routes', __name__)
bcrypt = Bcrypt()

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create new user
    user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    # Lookup user
    user = User.query.filter_by(email=data['email']).first()

    # Validate password
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    # If login fails
    return jsonify({"error": "Invalid credentials"}), 401


