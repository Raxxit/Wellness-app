from .extensions import db
from datetime import datetime

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


class Question(db.Model):
    __tablename__ = 'Questions'
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    type = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)

class QuestionOption(db.Model):
    __tablename__ = 'QuestionOptions'
    ROWID = db.Column(db.Integer, primary_key=True)
    option_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('Questions.question_id'))
    option_text = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

class WellnessResult(db.Model):
    __tablename__ = 'WellnessResults'
    result_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    total_score = db.Column(db.Integer, nullable=False)
    diagnosis_snapshot = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)