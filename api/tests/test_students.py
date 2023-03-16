import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.admin import Admin
from ..models.students import Student
from flask_jwt_extended import create_access_token

class UserTestCase(unittest.TestCase):
    
    def setUp(self):

        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()
        

    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_students(self):

        # Activate a test admin
        admin_signup_data = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com",
            "password": "password"
        }

        response = self.client.post('/admin/register', json=admin_signup_data)

        admin = Admin.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        
        # Register a student
        student_signup_data = {
            "first_name": "Test",
            "last_name": "Student",
            "email": "teststudent@gmail.com",
            "password": "password",
            "matric_no": "ZSCH/23/03/0001"
        }

        response = self.client.post('/students/register', json=student_signup_data, headers=headers)

        student = Student.query.filter_by(email='teststudent@gmail.com').first()

        assert student.first_name == "Test"

        assert student.matric_no == "ZSCH/23/03/0001"

        assert response.status_code == 201


        # Retrieve all students
        response = self.client.get('/students', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 2,
            "first_name": "Test",
            "last_name": "Student",
            "email": "teststudent@gmail.com",
            "matric_no": "ZSCH/23/03/0001",
            "user_type": "student"
        }]


        # Sign a student in
        student_login_data = {
            "email":"teststudent@gmail.com",
            "password": "password"
        }

        response = self.client.post('/auth/login', json=student_login_data)

        assert response.status_code == 201


        # Retrieve a student's details by ID
        response = self.client.get('/students/2', headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 2,
            "first_name": "Test",
            "last_name": "Student",
            "email": "teststudent@gmail.com",
            "matric_no": "ZSCH/23/03/0001",
            "user_type": "student"
        }


        # Update a student's details
        student_update_data = {
            "first_name": "Sample",
            "last_name": "Student",
            "email": "samplestudent@gmail.com",
            "password": "password"
        }

        response = self.client.put('/students/2', json=student_update_data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 2,
            "first_name": "Sample",
            "last_name": "Student",
            "email": "samplestudent@gmail.com",
            "matric_no": "ZSCH/23/03/0001",
            "user_type": "student"
        }


        # Register a test course
        course_registration_data = {
            "name": "Test Course",
            "teacher": "Test Teacher"
        }

        response = self.client.post('/courses', json=course_registration_data, headers=headers)


        # Enroll a student for a test course
        response = self.client.post('/courses/1/students/2', headers=headers)        


        # Retrieve a student's courses
        response = self.client.get('/students/2/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 1,
            "name": "Test Course",
            "teacher": "Test Teacher"
        }]

        # Upload a student's grade in a course
        grade_upload_data = {
            "student_id": 2,
            "course_id": 1,
            "percent_grade": 85.7
        }

        response = self.client.post('/students/2/grades', json=grade_upload_data, headers=headers)

        assert response.status_code == 201

        assert response.json == {
            "grade_id": 1,
            "student_id": 2,
            "student_first_name": "Sample",
            "student_last_name": "Student",
            "student_matric_no": "ZSCH/23/03/0001",
            "course_id": 1,
            "course_name": "Test Course",
            "course_teacher": "Test Teacher",
            "percent_grade": 85.7,
            "letter_grade": "B"
        } 


        # Retrieve a student's grades
        response = self.client.get('/students/2/grades', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "course_name": "Test Course",
            "grade_id": 1,
            "percent_grade": 85.7,
            "letter_grade": "B"
        }]


        # Update a grade
        grade_update_data = {
            "percent_grade": 91.5
        }

        response = self.client.put('/students/grades/1', json=grade_update_data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "grade_id": 1,
            "student_id": 2,
            "course_id": 1,
            "percent_grade": 91.5,
            "letter_grade": "A"
        }


        # Calculate a student's CGPA
        response = self.client.get('/students/2/cgpa', headers=headers)
        assert response.status_code == 200
        assert response.json["message"] == "Sample Student's CGPA is 4.0"


        # Delete a grade
        response = self.client.delete('/students/grades/1', headers=headers)
        assert response.status_code == 200


        # Delete a student
        response = self.client.delete('/students/2', headers=headers)
        assert response.status_code == 200