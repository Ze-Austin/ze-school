import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.admin import Admin
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


    def test_admin(self):

        # Register an admin
        admin_signup_data = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com",
            "password": "password"
        }

        response = self.client.post('/admin/register', json=admin_signup_data)

        admin = Admin.query.filter_by(email='testadmin@gmail.com').first()

        assert admin.first_name == "Test"

        assert admin.last_name == "Admin"

        assert response.status_code == 201
        

        # Sign an admin in
        admin_login_data = {
            "email":"testadmin@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/login', json=admin_login_data)

        assert response.status_code == 201

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }


        # Retrieve all admins
        response = self.client.get('/admin', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 1,
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com",
            "user_type": "admin"
        }]


        # Retrieve an admin's details by ID
        response = self.client.get('/admin/1', headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "first_name": "Test",
            "last_name": "Admin",
            "email": "testadmin@gmail.com",
            "user_type": "admin"
        }


        # Update an admin's details
        admin_update_data = {
            "first_name": "Sample",
            "last_name": "Admin",
            "email": "sampleadmin@gmail.com",
            "password": "password"
        }

        response = self.client.put('/admin/1', json=admin_update_data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "first_name": "Sample",
            "last_name": "Admin",
            "email": "sampleadmin@gmail.com",
            "user_type": "admin"
        }


        # Delete an admin
        response = self.client.delete('/admin/1', headers=headers)

        assert response.status_code == 200