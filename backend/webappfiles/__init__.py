from flask import Flask
import os
from .extensions import db, cors

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'superdummy8294r92y498'
    
    # Use relative path for SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/wellness.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Extensions
    db.init_app(app)
    cors.init_app(app)

    # Import and Register Blueprints
    from .auth import auth_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')

    return app