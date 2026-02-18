from flask import Blueprint, jsonify, request, current_app
from functools import wraps
import jwt
from .models import db, User, Appointment
from datetime import datetime

advisor_bp = Blueprint('advisor', __name__, url_prefix='/api/advisor')

# --- Helper: Token Decorator ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Token format is invalid!'}), 401
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                raise Exception("User not found")
        except Exception as e:
            return jsonify({'message': 'Token is invalid or expired!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# --- 1. Get Dashboard Data (MERGED AND FIXED) ---
@advisor_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_data(current_user):
    # Security Check
    if current_user.role != 'Advisor':
        return jsonify({'error': 'Unauthorized'}), 403

    # 1. Fetch Appointments for this Advisor
    appointments = Appointment.query.filter_by(advisor_id=current_user.id)\
        .order_by(Appointment.appointment_date.asc(), Appointment.appointment_time.asc()).all()

    # 2. Calculate Stats (From the first version)
    unique_clients = set(a.client_id for a in appointments)
    upcoming_count = sum(1 for a in appointments if a.status in ['Pending', 'Confirmed'])

    stats = {
        'total_clients': len(unique_clients),
        'upcoming_sessions': upcoming_count
    }

    # 3. Serialize Appointment Data (With client_id for the history button)
    appt_list = []
    for a in appointments:
        client = a.client
        appt_list.append({
            'id': a.appointment_id,
            'client_id': client.id if client else 0, # <--- IMPORTANT for "View Reports"
            'client_name': client.username if client else "Unknown User",
            'date': a.appointment_date,
            'time': a.appointment_time,
            'type': 'General Consultation', 
            'status': a.status,
            'notes': a.notes or '',
            'avatar': client.username[0].upper() if client else '?'
        })

    return jsonify({
        'stats': stats,
        'appointments': appt_list,
        'notifications': [], 
        'advisor_name': current_user.username
    })

# --- 2. Update Appointment ---
@advisor_bp.route('/appointment/<int:appt_id>/update', methods=['POST'])
@token_required
def update_appointment(current_user, appt_id):
    data = request.get_json()
    
    appt = Appointment.query.get(appt_id)
    if not appt or appt.advisor_id != current_user.id:
        return jsonify({'success': False, 'message': 'Appointment not found or unauthorized'}), 404

    try:
        if 'status' in data:
            appt.status = data['status']
        
        if 'notes' in data:
            appt.notes = data['notes']
            
        if 'date' in data:
            appt.appointment_date = data['date']
            
        if 'time' in data:
            appt.appointment_time = data['time']

        db.session.commit()
        return jsonify({'success': True, 'message': 'Appointment updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# --- 3. Get Patient History ---
@advisor_bp.route('/patient/<int:user_id>/history', methods=['GET'])
@token_required
def get_patient_history(current_user, user_id):
    
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404

    # MOCK DATA (You can connect this to real Task data later)
    history_data = [
        {'date': '2023-10-25', 'task': 'Morning Meditation', 'status': 'Completed', 'mood': 'Calm'},
        {'date': '2023-10-25', 'task': 'Journaling', 'status': 'Pending', 'mood': '-'},
        {'date': '2023-10-24', 'task': 'Drink 2L Water', 'status': 'Completed', 'mood': 'Energetic'},
        {'date': '2023-10-23', 'task': 'Walk 30 mins', 'status': 'Missed', 'mood': 'Tired'},
    ]

    return jsonify({
        'patient': {
            'name': target_user.username,
            'id': target_user.id,
            'riskLevel': 'Stable', 
            'email': target_user.email
        },
        'completionRate': 75,
        'history': history_data
    })