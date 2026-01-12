from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from .extensions import db
from .models import User

auth_bp = Blueprint('auth', __name__)

# LOGIN ROUTE
@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                "success": False,
                "message": "Email and password are required"
            }), 400
        
        email = data.get('email').strip().lower()
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
        
        if not check_password_hash(user.password_hash, password):
            return jsonify({
                "success": False,
                "message": "Invalid password"
            }), 401
        
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "age": user.age,
                "gender": user.gender
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Login error: {str(e)}"
        }), 500

@auth_bp.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "message": "Authentication service is running"
    }), 200





@auth_bp.route('/api/register', methods=['POST'])
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