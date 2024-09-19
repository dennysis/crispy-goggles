from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

# Role constants
USER_ROLES = ('Admin', 'Teacher', 'Parent', 'Student')

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_token(self, expires_in=3600):
        return create_access_token(identity=self.id, expires_delta=expires_in)

    def __repr__(self):
        return f'<User {self.username}>'

class Admin(User):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Admin',
    }
    
    def __repr__(self):
        return f'<Admin {self.email}>'


# Teacher Model
class Teacher(User):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    assignments = db.relationship('Homework', backref='teacher', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'Teacher',
    }
    
    def __repr__(self):
        return f'<Teacher {self.email}>'


class Parent(User):
    __tablename__ = 'parents'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    students = db.relationship('Student', foreign_keys='Student.parent_id', backref='parent_relationship', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'Parent',
    }
    
    def __repr__(self):
        return f'<Parent {self.email}>'

class Student(User):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    attendance_records = db.relationship('Attendance', backref='student', lazy=True)
    fee_records = db.relationship('Fee', backref='student', lazy=True)
    
    # Explicit relationship to Parent
    parent = db.relationship('Parent', foreign_keys=[parent_id], backref='children')
    
    __mapper_args__ = {
        'polymorphic_identity': 'Student',
    }
    
    def __repr__(self):
        return f'<Student {self.email}>'


class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Present, Absent, Late
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    
    def __repr__(self):
        return f'<Attendance {self.date} - {self.status}>'



class Homework(db.Model):
    __tablename__ = 'homework'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    student_submissions = db.relationship('HomeworkSubmission', backref='homework', lazy=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))

    def __repr__(self):
        return f'<Homework {self.title} - Due: {self.due_date}>'

class HomeworkSubmission(db.Model):
    __tablename__ = 'homework_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(10))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))

    def __repr__(self):
        return f'<Submission {self.id} - Grade: {self.grade}>'

class Fee(db.Model):
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    amount_due = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    paid_on = db.Column(db.Date)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __repr__(self):
        return f'<Fee {self.id} - Due: {self.amount_due}, Paid: {self.amount_paid}>'
