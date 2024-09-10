from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from config import db

class Parent(db.Model):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

    students = relationship('Student', backref='parent', lazy=True)
    payments = relationship('Payment', backref='parent', lazy=True)

class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    grade = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendees = relationship('Attendee', backref='student', lazy=True)
    results = relationship('Result', backref='student', lazy=True)
    homeworks = relationship('Homework', backref='student', lazy=True)
    payments = relationship('Payment', backref='student', lazy=True)
    # Association proxies
    attendee_dates = association_proxy('attendees', 'date_attended')
    result_scores = association_proxy('results', 'score')
    homework_titles = association_proxy('homeworks', 'title')
    payment_amounts = association_proxy('payments', 'amount')

    def __repr__(self):
        return f'<Student {self.name}>'

class Payment(db.Model):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)

    # Relationships
    parent = relationship('Parent', backref='payments')
    student = relationship('Student', backref='payments')

    def __repr__(self):
        return f'<Payment {self.amount} made on {self.payment_date}>'

class Attendee(db.Model):
    __tablename__ = 'attendees'  

    id = Column(Integer, primary_key=True)
    date_attended = Column(DateTime, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)

    # Relationship
    student = relationship('Student', backref='attendees')

    def __repr__(self):
        return f'<Attendee {self.student.name} attended on {self.date_attended}>'
