from .extensions import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    
    username = db.Column('user_name', db.Text, nullable=False)
    
    email = db.Column(db.Text, unique=True, nullable=False)
    
    password_hash = db.Column('password_hash', db.Text, nullable=False) 
    
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)

class Question(db.Model):
    __tablename__ = 'Questions'
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False) 
    is_active = db.Column(db.Boolean, default=True)
    
    options = db.relationship('QuestionOption', backref='question', lazy=True)

class QuestionOption(db.Model):
    __tablename__ = 'QuestionOptions'
    option_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('Questions.question_id'), nullable=False)
    option_text = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Integer, default=0) 

class DiagnosisLogic(db.Model):
    __tablename__ = 'DiagnosisLogic'
    logic_id = db.Column(db.Integer, primary_key=True)
    min_score = db.Column(db.Integer)
    max_score = db.Column(db.Integer)
    diagnosis_name = db.Column(db.String(100))
    severity_level = db.Column(db.String(50))
    advice_text = db.Column(db.Text)

class WellnessResult(db.Model):
    __tablename__ = 'WellnessResults'
    result_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    total_score = db.Column(db.Integer)
    diagnosis_snapshot = db.Column(db.String(255))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Resource(db.Model):
    __tablename__ = 'Resources'
    
    resource_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # video, article, podcast, app, website, game
    is_verified = db.Column(db.Integer, default=0)   # 0 for false, 1 for true
    added_by_admin_id = db.Column(db.Integer, nullable=True)  # Can be NULL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resource {self.title}>'