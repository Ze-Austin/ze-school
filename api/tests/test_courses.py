import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.courses import Course
from flask_jwt_extended import create_access_token

class CourseTestCase(unittest.TestCase):
    
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


    def test_course_retrieval(self):

        token = create_access_token(identity=1)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/courses/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == []
        

    def test_course_registration(self):

        data = {
            "name": "Test Course",
            "teacher": "Test Teacher"
        }

        token = create_access_token(identity=1)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post('/courses/courses', json=data, headers=headers)

        assert response.status_code == 201

        courses = Course.query.all()

        course_id = courses[0].id

        course_name = courses[0].name

        teacher = courses[0].teacher

        assert len(courses) == 1

        assert course_id == 1

        assert course_name == "Test Course"

        assert teacher == "Test Teacher"