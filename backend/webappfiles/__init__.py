from flask import Flask
from .extensions import db, cors

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wellness.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Extensions
    db.init_app(app)
    cors.init_app(app) # Allow Vue to talk to Flask

    # Import and Register Blueprints
    from .auth import auth_bp
    
    # Note: We use /api prefix so Vue knows these are data requests, not pages
    app.register_blueprint(auth_bp, url_prefix='/api')

    # Create Database Tables if they don't exist
    with app.app_context():
        db.create_all()

    return app