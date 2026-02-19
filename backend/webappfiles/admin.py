from flask import Blueprint, request, jsonify, send_from_directory, current_app, abort
from .extensions import db
from .models import User, Resource
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
    

@admin_bp.route('/resources', methods=['POST', 'OPTIONS'])
def create_resource():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        
        resource = Resource()
        resource.title = data.get('title')
        resource.url = data.get('url')
        resource.type = data.get('type')
        resource.is_verified = 1 if data.get('is_verified') else 0
        
        db.session.add(resource)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Resource created successfully",
            "id": resource.resource_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@admin_bp.route('/resources', methods=['GET'])
def get_resources():
    try:
        resources = Resource.query.order_by(Resource.created_at.desc()).all()
        
        result = []
        for r in resources:
            result.append({
                'resource_id': r.resource_id,
                'title': r.title,
                'url': r.url,
                'type': r.type,
                'is_verified': r.is_verified,
                'created_at': r.created_at.isoformat() if r.created_at else None
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    


@admin_bp.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
    try:
        resource = Resource.query.get_or_404(id)
        data = request.json
        
        # Update fields
        resource.title = data.get('title', resource.title)
        resource.url = data.get('url', resource.url)
        resource.type = data.get('type', resource.type)
        resource.is_verified = data.get('is_verified', resource.is_verified)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Resource updated successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    

@admin_bp.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    try:
        resource = Resource.query.get_or_404(id)
        db.session.delete(resource)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Resource deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500