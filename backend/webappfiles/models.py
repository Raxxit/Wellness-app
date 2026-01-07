from .extensions import db

class User(db.Model):
    # This line forces SQLAlchemy to use your EXISTING table from the screenshot
    __tablename__ = 'Users' 

    # Define columns exactly as they are in your SQLite database
    # Assuming these are the columns you created:
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.Text)   # Or db.String
    email = db.Column(db.Text, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.Text)
    password_hash = db.Column(db.Text) # Ensure you have a column for the password!
    
    # If your existing DB has different column names (e.g., 'user_name' instead of 'username'),
    # you must map them like this:
    # username = db.Column('user_name', db.String(100))