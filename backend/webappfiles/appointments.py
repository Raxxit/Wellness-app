from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import jwt
from .models import db, User, Appointment

appointment_bp = Blueprint('appointment', __name__, url_prefix='/api/appointments')

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


# --- 2. Routes ---

@appointment_bp.route('/advisors', methods=['GET'])
@token_required
def get_advisors(current_user):
    advisors = User.query.filter_by(role='Advisor', is_verified=True).all()
    
    advisor_list = [{
        'id': a.id,
        'name': a.username, 
        'bio': a.bio
    } for a in advisors]
    
    return jsonify(advisor_list)


@appointment_bp.route('/book', methods=['POST'])
@token_required
def book_appointment(current_user):
    data = request.get_json()
    
    advisor_id = data.get('advisor_id')
    date = data.get('date')
    time = data.get('time')
    notes = data.get('notes')

    if not all([advisor_id, date, time]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    try:
        new_appt = Appointment(
            client_id=current_user.id,
            advisor_id=advisor_id,
            appointment_date=date,
            appointment_time=time,
            notes=notes,
            status='Pending'
        )
        
        db.session.add(new_appt)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Appointment requested successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@appointment_bp.route('/my-appointments', methods=['GET'])
@token_required
def get_my_appointments(current_user):
    appointments = Appointment.query.filter_by(client_id=current_user.id).order_by(Appointment.appointment_id.desc()).all()
    
    results = []
    for appt in appointments:
        results.append({
            'id': appt.appointment_id,
            'advisor_name': appt.advisor.username if appt.advisor else "Unknown Advisor",
            'date': appt.appointment_date,
            'time': appt.appointment_time,
            'status': appt.status,
            'notes': appt.notes
        })
    
    return jsonify(results)