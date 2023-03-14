from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.admin import Admin
from ..utils.decorators import admin_required
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity

admin_namespace = Namespace('admin', description='Namespace for Administrators')

admin_signup_model = admin_namespace.model(
    'AdminSignup', {
        'first_name': fields.String(required=True, description="Admin's First Name"),
        'last_name': fields.String(required=True, description="Admin's Last Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'password': fields.String(required=True, description="Admin's Password")
    }
)

admin_model = admin_namespace.model(
    'Admin', {
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'password_hash': fields.String(required=True, description="Admin's Password"),  
        'user_type': fields.String(required=True, description="Type of User")
    }
)

@admin_namespace.route('')
class GetAllAdmins(Resource):

    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description="Retrieve all admins"
    )
    @admin_required()
    def get(self):
        """
            Retrieve all Admins - Admins Only`
        """
        admins = Admin.query.all()

        return admins, HTTPStatus.OK

@admin_namespace.route('/register')
class AdminRegistration(Resource):

    @admin_namespace.expect(admin_signup_model)
    @admin_namespace.marshal_with(admin_model)
    def post(self):
        """
            Register an Admin 
        """        
        data = request.get_json()

        new_admin = Admin(
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password')),
            user_type = 'admin'
        )

        new_admin.save()

        return new_admin, HTTPStatus.CREATED

@admin_namespace.route('/<int:admin_id>')
class GetUpdateDeleteAdmins(Resource):
    
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description="Retrieve an admin's details by ID",
        params = {
            'admin_id': "The admin's ID"
        }
    )
    @admin_required()
    def get(self, admin_id):
        """
            Retrieve an Admin's Details by ID - Admins Only
        """
        admin = Admin.get_by_id(admin_id)
        
        return admin, HTTPStatus.OK
    
    @admin_namespace.expect(admin_signup_model)
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description="Update an admin's details by ID",
        params = {
            'admin_id': "The Admin's ID"
        }
    )
    @admin_required()
    def put(self, admin_id):
        """
            Update an Admin's Details by ID - Admins Only
        """
        admin = Admin.get_by_id(admin_id)
        active_admin = get_jwt_identity()
        if active_admin != admin:
            return 

        data = admin_namespace.payload

        admin.first_name = data['first_name']
        admin.last_name = data['last_name']
        admin.email = data['email']
        admin.password_hash = generate_password_hash(data['password'])

        admin.update()

        return admin, HTTPStatus.OK
    
    @admin_namespace.doc(
        description='Delete an admin by ID',
        params = {
            'admin_id': "The Admin's ID"
        }
    )
    @admin_required()
    def delete(self, admin_id):
        """
            Delete an Admin by ID - Admins Only
        """
        admin = Admin.get_by_id(admin_id)

        admin.delete()

        return {"message": "Admin Successfully Deleted"}, HTTPStatus.OK