from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from .extensions import db
from .models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    
    # 1. Get data using standard form keys
    username = request.form.get('username')
    email = request.form.get('email')
    age = request.form.get('age')
    gender = request.form.get('gender')
    password = request.form.get('password')

    # Basic Validation
    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # 2. Check if user exists (using your existing DB)
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    # 3. Hash Password
    hashed_pw = generate_password_hash(password)

    # 4. Create User Object
    new_user = User(
        username=username,
        email=email,
        age=age,
        gender=gender,
        password_hash=hashed_pw
    )

    # 5. Save to your existing 'Users' table
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500