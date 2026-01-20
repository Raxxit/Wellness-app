from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from .extensions import db
from .models import User, Question, QuestionOption, WellnessResult, DiagnosisLogic

auth_bp = Blueprint('auth', __name__)

# LOGIN ROUTE
@auth_bp.route('/login', methods=['POST'])
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


@auth_bp.route('/profile/update', methods=['PUT'])
def update_profile():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "success": False,
                "message": "Authorization required"
            }), 401
        
        token = auth_header.split(' ')[1]
        
        try:
            decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = decoded['user_id']
        except:
            return jsonify({
                "success": False,
                "message": "Invalid token"
            }), 401
        
        # Get user from database
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
        
        # Get update data
        data = request.get_json()
        
        # Update user fields
        if 'username' in data and data['username']:
            user.username = data['username']
        
        if 'age' in data:
            # Allow age to be null
            user.age = data['age'] if data['age'] else None
        
        if 'gender' in data:
            # Allow gender to be null
            user.gender = data['gender'] if data['gender'] else None
        
        if 'password' in data and data['password']:
            # Update password if provided
            user.password_hash = generate_password_hash(data['password'])
        
        # Save changes to database
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "age": user.age,
                "gender": user.gender
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Update error: {str(e)}"
        }), 500

# GET PROFILE ROUTE
@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    try:
        # Get authorization token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "success": False,
                "message": "Authorization required"
            }), 401
        
        token = auth_header.split(' ')[1]
        
        # Decode token to get user ID
        try:
            decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = decoded['user_id']
        except:
            return jsonify({
                "success": False,
                "message": "Invalid token"
            }), 401
        
        # Get user from database
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
        
        return jsonify({
            "success": True,
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
            "message": f"Profile error: {str(e)}"
        }), 500

# LOGOUT ROUTE (optional)
@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200



@auth_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "message": "Authentication service is running"
    }), 200





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
    


    

    # 1. ADMIN: Add a new Question
@auth_bp.route('/add-question', methods=['POST'])
def add_question():
    data = request.json
    
    # Create the Question
    new_q = Question(
        question_text=data['text'],
        type=data['type'],
        is_active=True
    )
    db.session.add(new_q)
    db.session.flush() # Flush to get the new question_id before committing
    
    for opt in data['options']:
        new_opt = QuestionOption(
            question_id=new_q.question_id,
            option_text=opt['text'],
            weight=int(opt['weight'])
        )
        db.session.add(new_opt)
        
    db.session.commit()
    return jsonify({"message": "Question added", "id": new_q.question_id})

# 2. USER: Get Questionnaire
@auth_bp.route('/questionnaire', methods=['GET'])
def get_questionnaire():
    questions = Question.query.filter_by(is_active=True).all()
    output = []
    
    for q in questions:
        options = [{'id': o.option_id, 'text': o.option_text, 'weight': o.weight} for o in q.options]
        output.append({
            'id': q.question_id,
            'text': q.question_text,
            'type': q.type,
            'options': options
        })
        
    return jsonify(output)

@auth_bp.route('/submit-wellness', methods=['POST'])
def submit_wellness():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded['user_id']
    except:
        return jsonify({"message": "Invalid token"}), 401

    data = request.json
    selected_option_ids = data.get('selected_options', [])
    
    total_score = 0
    if selected_option_ids:
        selected_options = QuestionOption.query.filter(
            QuestionOption.option_id.in_(selected_option_ids)
        ).all()
        total_score = sum(opt.weight for opt in selected_options)
    

    diagnosis = DiagnosisLogic.query.filter(
        DiagnosisLogic.min_score <= total_score,
        DiagnosisLogic.max_score >= total_score
    ).first()
    
    diag_name = diagnosis.diagnosis_name if diagnosis else "General Wellness"
    advice = diagnosis.advice_text if diagnosis else "Keep maintaining a healthy lifestyle."
    
    try:
        result = WellnessResult(
            user_id=user_id, 
            total_score=total_score,
            diagnosis_snapshot=diag_name
        )
        db.session.add(result)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "score": total_score, 
            "diagnosis": diag_name, 
            "advice": advice
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    data = request.json
    selected_option_ids = data.get('selected_options', [])
    
    total_score = 0
    if selected_option_ids:
        selected_options = QuestionOption.query.filter(QuestionOption.option_id.in_(selected_option_ids)).all()
        total_score = sum(opt.weight for opt in selected_options)
    
    diagnosis = DiagnosisLogic.query.filter(
        DiagnosisLogic.min_score <= total_score,
        DiagnosisLogic.max_score >= total_score
    ).first()
    
    diag_name = diagnosis.diagnosis_name if diagnosis else "Unknown"
    
    result = WellnessResult(
        user_id=data.get('user_id'),
        total_score=total_score,
        diagnosis_snapshot=diag_name
    )
    db.session.add(result)
    db.session.commit()
    
    return jsonify({
        "score": total_score, 
        "diagnosis": diag_name, 
        "advice": diagnosis.advice_text if diagnosis else ""
    })


@auth_bp.route('/wellness-history', methods=['GET'])
def wellness_history():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:

        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user_id = decoded['user_id']
    except:
        return jsonify({"message": "Invalid token"}), 401


    results = WellnessResult.query.filter_by(user_id=current_user_id)\
        .order_by(WellnessResult.generated_at.desc())\
        .all()
    
    history_data = []
    for r in results:
        history_data.append({
            "id": r.result_id,
            "score": r.total_score,
            "diagnosis": r.diagnosis_snapshot, # e.g., "High Wellness"
            # Format datetime to string (YYYY-MM-DD)
            "date": r.generated_at.strftime("%Y-%m-%d") if r.generated_at else "N/A"
        })
        
    return jsonify(history_data), 200


@auth_bp.route('/dashboard-stats', methods=['GET'])
def dashboard_stats():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization required"}), 401
    
    try:
        token = auth_header.split(' ')[1]
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded['user_id']
    except:
        return jsonify({"message": "Invalid token"}), 401

    assessment_count = WellnessResult.query.filter_by(user_id=user_id).count()

    return jsonify({
        "assessments_completed": assessment_count
    }), 200