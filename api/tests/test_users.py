import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.users import User
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


    def test_user_registration(self):

        data = {
            "name": "Test User",
            "email": "testuser@gmail.com",
            "password": "password"
        }

        response = self.client.post('/auth/signup', json=data)

        user = User.query.filter_by(email='testuser@gmail.com').first()

        assert user.name == "Test User"

        assert response.status_code == 201


    def test_user_login(self):

        data = {
            "email":"testuser@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/login', json=data)

        assert response.status_code == 200

    
    def test_user_retrieval(self):

        token = create_access_token(identity=1)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get('/auth/users', headers=headers)

        assert response.status_code == 200

        assert response.json == []