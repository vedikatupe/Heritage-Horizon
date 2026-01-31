from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.db import db
from src.models.models import User  # Assuming you have a User model defined

def register_user(username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully."}), 201

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials."}), 401
    # Here you would typically generate a token for the user
    return jsonify({"message": "Login successful."}), 200

def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404
    return jsonify({"username": user.username}), 200