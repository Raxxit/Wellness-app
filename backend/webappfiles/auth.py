from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from .extensions import db
from .models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    
    username = request.form.get('username')
    email = request.form.get('email')
    age = request.form.get('age', type=int)
    gender = request.form.get('gender', type=int)
    password = request.form.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    hashed_pw = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        age=age,
        gender=gender,
        password_hash=hashed_pw
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500