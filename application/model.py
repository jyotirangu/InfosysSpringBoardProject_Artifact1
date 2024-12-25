from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    _tablename_ = 'Infosys_user'  # Table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)  # Password should be hashed
    role = db.Column(db.String(50), nullable=False, default='basic')
    isVerified = db.Column(db.String(20), nullable=False)
    answer = db.Column(db.String(50), nullable=False)
    

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)

    # Foreign key referencing User table
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)