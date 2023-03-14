import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
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


    def test_student_registration(self):

        data = {
            "first_name": "Test",
            "last_name": "Student",
            "email": "teststudent@gmail.com",
            "password": "password",
            "matric_no": "ZSCH/23/03/0001"
        }

        response = self.client.post('/students/register', json=data, headers=headers)

        student = Student.query.filter_by(email='teststudent@gmail.com').first()

        assert student.first_name == "Test"

        assert student.matric_no == "ZSCH/23/03/0001"

        assert response.status_code == 201


    def test_student_login(self):

        data = {
            "email":"teststudent@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/login', json=data)

        assert response.status_code == 200

    
    def test_student_retrieval(self):

        token = create_access_token(identity=1)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/students', headers=headers)

        assert response.status_code == 200

        assert response.json == []