from flask import Blueprint, request, jsonify
from app.models import Teacher, Student, Homework, HomeworkSubmission
from app import db
from datetime import datetime

teacher_bp = Blueprint('teacher', __name__)

# Assign homework
@teacher_bp.route('/assign_homework', methods=['POST'])
def assign_homework():
    data = request.get_json()

    # Validate input
    if not data or 'title' not in data or 'description' not in data or 'due_date' not in data or 'student_id' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    title = data['title']
    description = data['description']
    due_date = data['due_date']
    student_id = data['student_id']

    # Check if the student exists
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    # Create new homework entry
    new_homework = Homework(title=title, description=description, due_date=datetime.strptime(due_date, '%Y-%m-%d'), student_id=student_id)
    db.session.add(new_homework)
    db.session.commit()

    return jsonify({'message': 'Homework assigned successfully'}), 201

# View student progress
@teacher_bp.route('/view_progress/<int:student_id>', methods=['GET'])
def view_progress(student_id):
    # Get all homework submissions for the student
    submissions = HomeworkSubmission.query.filter_by(student_id=student_id).all()
    
    if not submissions:
        return jsonify({'message': 'No submissions found for this student'}), 404

    progress = []
    for submission in submissions:
        progress.append({
            'homework_id': submission.homework_id,
            'score': submission.score,
            'submitted_at': submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Submitted' if submission.score is not None else 'Not Submitted'
        })

    return jsonify({'student_id': student_id, 'progress': progress}), 200
