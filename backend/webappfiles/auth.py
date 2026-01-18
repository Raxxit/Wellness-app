from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from .extensions import db
from .models import User, Question, QuestionOption, WellnessResult

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

@auth_bp.route('health', methods=['GET'])
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
    


  # GET all active questions with options
@auth_bp.route('/questionnaire/questions', methods=['GET'])
def get_questions():
    try:
        # Check if user is authenticated
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Authentication required'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['user_id']
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        # CHANGED: is_active=1 instead of is_active=True
        questions = Question.query.filter_by(is_active=1).all()
        
        questions_data = []
        for question in questions:
            options = QuestionOption.query.filter_by(question_id=question.question_id).all()
            
            options_data = [
                {
                    'option_id': opt.option_id,
                    'option_text': opt.option_text,
                    'weight': opt.weight
                }
                for opt in options
            ]
            
            questions_data.append({
                'question_id': question.question_id,
                'question_text': question.question_text,
                'type': question.type,
                'options': options_data
            })
        
        return jsonify({
            'success': True,
            'questions': questions_data
        }), 200
        
    except Exception as e:
        print(f"Error in get_questions: {str(e)}")  # ADD THIS FOR DEBUG
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


# POST - Submit questionnaire answers
@auth_bp.route('/questionnaire/submit', methods=['POST'])
def submit_questionnaire():
    try:
        # Check authentication
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Authentication required'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['user_id']
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        # Get answers from request
        request_data = request.get_json()
        answers = request_data.get('answers')
        
        if not answers:
            return jsonify({'success': False, 'message': 'No answers provided'}), 400
        
        # Calculate total score
        total_score = 0
        diagnosis_details = []
        
        for answer in answers:
            question_id = answer.get('question_id')
            option_id = answer.get('option_id')
            
            option = QuestionOption.query.filter_by(
                question_id=question_id,
                option_id=option_id
            ).first()
            
            if option:
                total_score += option.weight
                question = Question.query.get(question_id)
                diagnosis_details.append({
                    'question': question.question_text,
                    'answer': option.option_text,
                    'weight': option.weight
                })
        
        # Calculate result level (1-5)
        num_questions = len(answers)
        max_score = num_questions * 5
        percentage = (total_score / max_score) * 100
        
        if percentage <= 20:
            result_level = 1
        elif percentage <= 40:
            result_level = 2
        elif percentage <= 60:
            result_level = 3
        elif percentage <= 80:
            result_level = 4
        else:
            result_level = 5
        
        # Get interpretation
        interpretations = {
            1: "You may be experiencing significant challenges. We recommend connecting with professional support.",
            2: "You're facing some difficulties. Let's work together on improving your wellness.",
            3: "You're doing okay, but there's room for improvement. Small steps can make a big difference.",
            4: "You're doing well! Keep up the good habits and continue your wellness journey.",
            5: "Excellent! You're thriving. Maintain these positive practices."
        }
        interpretation = interpretations.get(result_level, "Assessment complete")
        
        # Create diagnosis snapshot
        diagnosis_snapshot = str({
            'result_level': result_level,
            'total_score': total_score,
            'max_score': max_score,
            'percentage': round(percentage, 2),
            'answers': diagnosis_details,
            'interpretation': interpretation
        })
        
        # Save to database
        wellness_result = WellnessResult(
            user_id=user_id,
            total_score=total_score,
            diagnosis_snapshot=diagnosis_snapshot,
            generated_at=datetime.datetime.utcnow()
        )
        
        db.session.add(wellness_result)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Questionnaire submitted successfully',
            'result': {
                'result_id': wellness_result.result_id,
                'result_level': result_level,
                'total_score': total_score,
                'max_score': max_score,
                'percentage': round(percentage, 2),
                'interpretation': interpretation
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


# GET user's latest result
@auth_bp.route('/questionnaire/results/latest', methods=['GET'])
def get_latest_result():
    try:
        # Check authentication
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Authentication required'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['user_id']
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        result = WellnessResult.query.filter_by(user_id=user_id)\
            .order_by(WellnessResult.generated_at.desc()).first()
        
        if not result:
            return jsonify({'success': False, 'message': 'No results found'}), 404
        
        return jsonify({
            'success': True,
            'result': {
                'result_id': result.result_id,
                'total_score': result.total_score,
                'diagnosis_snapshot': result.diagnosis_snapshot,
                'generated_at': result.generated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500