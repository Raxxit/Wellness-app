from flask import Flask
import os
from .extensions import db, cors

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'superdummy8294r92y498'
    

    basedir = os.path.abspath(os.path.dirname(__file__))
    

    db_path = os.path.join(os.path.dirname(basedir), 'instance', 'wellness.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    cors.init_app(app)

    from .auth import auth_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')

    return app