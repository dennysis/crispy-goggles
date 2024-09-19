from flask import Blueprint, request, jsonify
from app.models import Admin, User, Homework, Attendance
from app import db
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

# Create a new user (Admin, Teacher, Parent/Student)
@admin_bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validate input
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    username = data['username']
    password = data['password']
    role = data['role']

    # Check if the user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409

    # Create a new user
    new_user = User(username=username, password=generate_password_hash(password), role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Get attendance report
@admin_bp.route('/attendance_report', methods=['GET'])
def attendance_report():
    # Query attendance data (you can filter by date, class, etc.)
    attendance_records = Attendance.query.all()
    report = []

    for record in attendance_records:
        report.append({
            'student_id': record.student_id,
            'date': record.date,
            'status': record.status
        })

    return jsonify({'attendance_report': report}), 200

# Upload results
@admin_bp.route('/upload_results', methods=['POST'])
def upload_results():
    data = request.get_json()

    # Validate input
    if not data or 'student_id' not in data or 'subject' not in data or 'score' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    student_id = data['student_id']
    subject = data['subject']
    score = data['score']

    # Here you could add logic to check if the student exists, validate the score, etc.

    # Create a new homework or results entry (assuming you have a model for this)
    new_result = Homework(student_id=student_id, subject=subject, score=score)
    db.session.add(new_result)
    db.session.commit()

    return jsonify({'message': 'Results uploaded successfully'}), 201
