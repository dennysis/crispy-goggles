from flask import Blueprint, request, jsonify
from app.models import Student, Homework, HomeworkSubmission
from app import db

parent_bp = Blueprint('parent', __name__)

# View Homework
@parent_bp.route('/view_homework/<int:student_id>', methods=['GET'])
def view_homework(student_id):
    # Get the student's homework
    homework_list = Homework.query.filter_by(student_id=student_id).all()

    if not homework_list:
        return jsonify({'message': 'No homework found for this student'}), 404

    homework_data = []
    for homework in homework_list:
        homework_data.append({
            'homework_id': homework.id,
            'title': homework.title,
            'description': homework.description,
            'due_date': homework.due_date.strftime('%Y-%m-%d'),
            'status': 'Submitted' if homework.submissions else 'Not Submitted'
        })

    return jsonify({'student_id': student_id, 'homework': homework_data}), 200

# Submit Homework
@parent_bp.route('/submit_homework', methods=['POST'])
def submit_homework():
    data = request.get_json()

    # Validate input
    if not data or 'homework_id' not in data or 'student_id' not in data or 'score' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    homework_id = data['homework_id']
    student_id = data['student_id']
    score = data['score']

    # Check if the homework exists
    homework = Homework.query.get(homework_id)
    if not homework:
        return jsonify({'message': 'Homework not found'}), 404

    # Create new homework submission
    new_submission = HomeworkSubmission(homework_id=homework_id, student_id=student_id, score=score)
    db.session.add(new_submission)
    db.session.commit()

    return jsonify({'message': 'Homework submitted successfully'}), 201
