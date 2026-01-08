from .extensions import db

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    
    username = db.Column('user_name', db.Text, nullable=False)
    
    email = db.Column(db.Text, unique=True, nullable=False)
    
    # --- CHANGED LINE BELOW ---
    # We changed 'password' to 'password_hash' to match your actual database
    password_hash = db.Column('password_hash', db.Text, nullable=False) 
    
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)