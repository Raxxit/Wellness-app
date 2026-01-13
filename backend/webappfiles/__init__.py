from flask import Flask
import os
from .extensions import db, cors

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dummylmao'
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Go up one level to 'backend' and then into 'instance'
    # Result: .../backend/instance/wellness.db
    db_path = os.path.join(os.path.dirname(base_dir), 'instance', 'wellness.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    # --- FIX END ---
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Extensions
    db.init_app(app)
    cors.init_app(app)

    # Import and Register Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')

    return app