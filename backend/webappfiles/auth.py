from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import jwt, re, logging, datetime, os, uuid
from .extensions import db
from .models import User, Question, QuestionOption, WellnessResult, DiagnosisLogic

auth_bp = Blueprint('auth', __name__)

# --- UTILITY: TOKEN DECODER ---
def decode_token(auth_header):
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    try:
        token = auth_header.split(' ')[1]
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return None

# --- AUTH ROUTES ---

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        email = data.get('email').strip().lower()
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
            
        if user.role == 'Advisor' and not user.is_verified:
            return jsonify({"success": False, "message": "Advisor account pending verification."}), 403
        
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "success": True,
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    if not request.form:
        return jsonify({"success": False, "message": "No form data"}), 400

    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    
    try:
        age = int(request.form.get('age'))
        gender = int(request.form.get('gender'))
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid age/gender format"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email already exists", "field": "email"}), 409

    new_user = User(
        username=username,
        email=email,
        age=age, 
        gender=gender, 
        password_hash=generate_password_hash(password)
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True, "message": "User registered successfully"}), 200

# --- WELLNESS & QUESTIONNAIRE ROUTES ---

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
    decoded = decode_token(request.headers.get('Authorization'))
    if not decoded:
        return jsonify({"message": "Authorization required"}), 401

    data = request.json
    selected_option_ids = data.get('selected_options', [])
    
    # Calculate Score
    selected_options = QuestionOption.query.filter(QuestionOption.option_id.in_(selected_option_ids)).all()
    total_score = sum(opt.weight for opt in selected_options)

    # Find Diagnosis Logic
    diagnosis = DiagnosisLogic.query.filter(
        DiagnosisLogic.min_score <= total_score,
        DiagnosisLogic.max_score >= total_score
    ).first()
    
    diag_name = diagnosis.diagnosis_name if diagnosis else "General Wellness"
    advice = diagnosis.advice_text if diagnosis else "Keep maintaining a healthy lifestyle."
    
    try:
        result = WellnessResult(
            user_id=decoded['user_id'], 
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

@auth_bp.route('/wellness-history', methods=['GET'])
def wellness_history():
    decoded = decode_token(request.headers.get('Authorization'))
    if not decoded:
        return jsonify({"message": "Authorization required"}), 401

    results = WellnessResult.query.filter_by(user_id=decoded['user_id'])\
        .order_by(WellnessResult.generated_at.desc()).all()
    
    history_data = []
    for r in results:
        logic_entry = DiagnosisLogic.query.filter(
            DiagnosisLogic.min_score <= r.total_score,
            DiagnosisLogic.max_score >= r.total_score
        ).first()

        history_data.append({
            "id": r.result_id,
            "score": r.total_score,
            "diagnosis": r.diagnosis_snapshot, 
            "advice": logic_entry.advice_text if logic_entry else "N/A",
            "date": r.generated_at.strftime("%Y-%m-%d") if r.generated_at else "N/A"
        })
    return jsonify(history_data), 200

@auth_bp.route('/dashboard-stats', methods=['GET'])
def dashboard_stats():
    decoded = decode_token(request.headers.get('Authorization'))
    if not decoded:
        return jsonify({"message": "Authorization required"}), 401

    assessment_count = WellnessResult.query.filter_by(user_id=decoded['user_id']).count()
    return jsonify({"assessments_completed": assessment_count}), 200

# --- PROFESSIONAL REGISTRATION ---

@auth_bp.route('/register-professional', methods=['POST'])
def register_professional():
    if not request.form:
        return jsonify({"success": False, "message": "No form data"}), 400
    
    email = request.form.get('email', '').strip().lower()
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email taken"}), 409

    if 'related_docs' not in request.files:
        return jsonify({"success": False, "message": "No document uploaded"}), 400
    
    file = request.files['related_docs']
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    upload_folder = os.path.join('uploads', 'professionals')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)

    new_user = User(
        username=request.form.get('username'),
        email=email,
        age=int(request.form.get('age')),
        gender=int(request.form.get('gender')),
        password_hash=generate_password_hash(request.form.get('password')),
        role="Advisor",
        related_docs=unique_filename,
        bio=request.form.get('bio'),
        is_verified=False
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": True, "message": "Registration successful"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Server error"}), 500

# --- ADMIN / MAINTENANCE ---

@auth_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200


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



@auth_bp.route('/delete-question/<int:q_id>', methods=['DELETE'])
def delete_question(q_id):
    try:
        # Find the question
        question = Question.query.get(q_id)
        if not question:
            return jsonify({"success": False, "message": "Question not found"}), 404
            
        QuestionOption.query.filter_by(question_id=q_id).delete()
        db.session.delete(question)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Question deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500