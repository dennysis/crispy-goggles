from flask import Blueprint, request, jsonify
from app.models import Admin, User, Homework, Attendance, Student, HomeworkSubmission, Teacher, Parent
from app import db
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    print("Received data:", data)  # Debugging line

    # Validate input
    if not data or 'username' not in data or 'email' not in data or 'password' not in data or 'role' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    username = data['username']
    email = data['email']
    password = data['password']
    role = data['role']

    # Ensure the email and username are unique
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already taken'}), 409

    # Validate role
    if role not in ['Admin', 'Teacher', 'Parent', 'Student']:
        return jsonify({'message': 'Invalid role'}), 400

    try:
        # Create a new user
        new_user = User(username=username, email=email, password=generate_password_hash(password), role=role)
        db.session.add(new_user)
        db.session.commit()

        # Create role-specific user
        role_user = None
        if role == 'Admin':
            role_user = Admin(id=new_user.id)
        elif role == 'Teacher':
            role_user = Teacher(id=new_user.id)
        elif role == 'Parent':
            role_user = Parent(id=new_user.id)
        elif role == 'Student':
            role_user = Student(id=new_user.id)

        if role_user:
            db.session.add(role_user)
            db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        print("Error during user creation:", e)  # Log the error
        return jsonify({'message': 'Could not create user'}), 500

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
    if not data or 'student_id' not in data or 'homework_id' not in data or 'grade' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    student_id = data['student_id']
    homework_id = data['homework_id']
    grade = data['grade']

    # Check if the student and homework exist
    student = Student.query.get(student_id)
    homework = Homework.query.get(homework_id)
    if not student or not homework:
        return jsonify({'message': 'Student or Homework not found'}), 404

    # Create a new homework submission
    new_submission = HomeworkSubmission(student_id=student_id, homework_id=homework_id, grade=grade)
    db.session.add(new_submission)
    db.session.commit()

    return jsonify({'message': 'Results uploaded successfully'}), 201
