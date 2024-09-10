#!/usr/bin/env python3

# Remote library imports
from flask import request, Flask
from flask_restful import Resource, Api
from config import app, db, api

# Local imports
from models import Student

# Define your API resources
class StudentResource(Resource):
    def get(self):
        students = Student.query.all()
        return [student.to_dict() for student in students]

    def post(self):
        data = request.get_json()
        new_student = Student(
            name=data['name'],
            grade=data['grade'],
            parent_id=data['parent_id']
        )
        db.session.add(new_student)
        db.session.commit()
        return new_student.to_dict(), 201

# Add routes to the API
api.add_resource(StudentResource, '/students')

# Root route
@app.route('/')
def index():
    return '<h1>Project Server</h1>'

# Run the application
if __name__ == '__main__':
    app.run(port=5555, debug=True)
