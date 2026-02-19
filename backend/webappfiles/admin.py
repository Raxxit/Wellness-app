from flask import Blueprint, request, jsonify, send_from_directory, current_app, abort
from .extensions import db
from .models import User
from datetime import datetime
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/pending-advisors', methods=['GET'])
def get_pending_pros():
    pending_users = User.query.filter(User.role == 'Advisor', User.is_verified == False).all()    
    
    users_data = []
    for u in pending_users:
        users_data.append({
            'user_id': u.id,
            'user_name': u.username,
            'email': u.email,
            'age': u.age,
            'gender': ['other', 'Male','Female'][u.gender] if u.gender is not None else 'N/A',
            'bio': u.bio,
            'related_docs': u.related_docs, 
            'created_at': u.created_at.strftime('%Y-%m-%d')
        })
    
    return jsonify(users_data)

@admin_bp.route('/verify-user/<int:user_id>', methods=['POST'])
def verify_user(user_id):
    data = request.json
    action = data.get('action') 
    
    user = User.query.get_or_404(user_id)
    
    if action == 'approve':
        user.is_verified = True
        msg = "User verified successfully."
    elif action == 'reject':
        user.role = 'User'
        user.is_verified = False
        msg = "Application rejected. User downgraded to standard role."
    else:
        return jsonify({"success": False, "message": "Invalid action"}), 400

    try:
        db.session.commit()
        return jsonify({"success": True, "message": msg})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


import os
from flask import send_from_directory, current_app

@admin_bp.route('/document/<filename>')
def get_document(filename):
    app_root = current_app.root_path
    
    directory = os.path.abspath(os.path.join(app_root, '..', 'uploads', 'professionals'))
    
    print(f"DEBUG: Serving from: {directory}")

    try:
        return send_from_directory(directory, filename)
    except FileNotFoundError:
        return jsonify({"success": False, "message": "File not found"}), 404