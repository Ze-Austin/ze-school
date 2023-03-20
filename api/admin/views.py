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
        'id': fields.Integer(description="Admin's User ID"),
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'user_type': fields.String(required=True, description="Type of User")
    }
)

@admin_namespace.route('')
class GetAllAdmins(Resource):

    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description="Retrieve All Admins - Admins Only"
    )
    @admin_required()
    def get(self):
        """
            Retrieve All Admins - Admins Only
        """
        admins = Admin.query.all()

        return admins, HTTPStatus.OK

@admin_namespace.route('/register')
class AdminRegistration(Resource):

    @admin_namespace.expect(admin_signup_model)
    # Uncomment the @admin_required() decorator below after registering the first admin
    # This ensures that only an existing admin can register a new admin account on the app
    # @admin_required()
    @admin_namespace.doc(
        description = "Register an Admin - Admins Only, after First Admin"
    )
    def post(self):
        """
            Register an Admin - Admins Only, after First Admin
        """        
        data = admin_namespace.payload

        # Check if the admin account already exists
        admin = Admin.query.filter_by(email=data['email']).first()
        if admin:
            return {"message": "Admin Account Already Exists"}, HTTPStatus.CONFLICT

        # Register new admin
        new_admin = Admin(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            user_type = 'admin'
        )

        new_admin.save()

        admin_resp = {}
        admin_resp['id'] = new_admin.id
        admin_resp['first_name'] = new_admin.first_name
        admin_resp['last_name'] = new_admin.last_name
        admin_resp['email'] = new_admin.email
        admin_resp['user_type'] = new_admin.user_type

        return admin_resp, HTTPStatus.CREATED

@admin_namespace.route('/<int:admin_id>')
class GetUpdateDeleteAdmins(Resource):
    
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description = "Retrieve an Admin's Details by ID - Admins Only",
        params = {
            'admin_id': "The Admin's ID"
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
    @admin_namespace.doc(
        description = "Update an Admin's Details by ID - Specific Admin Only",
        params = {
            'admin_id': "The Admin's ID"
        }
    )
    @admin_required()
    def put(self, admin_id):
        """
            Update an Admin's Details by ID - Specific Admin Only
        """
        admin = Admin.get_by_id(admin_id)
        active_admin = get_jwt_identity()
        if active_admin != admin_id:
            return {"message": "Specific Admin Only"}, HTTPStatus.FORBIDDEN

        data = admin_namespace.payload

        admin.first_name = data['first_name']
        admin.last_name = data['last_name']
        admin.email = data['email']
        admin.password_hash = generate_password_hash(data['password'])

        admin.update()

        admin_resp = {}
        admin_resp['id'] = admin.id
        admin_resp['first_name'] = admin.first_name
        admin_resp['last_name'] = admin.last_name
        admin_resp['email'] = admin.email
        admin_resp['user_type'] = admin.user_type

        return admin_resp, HTTPStatus.OK
    
    @admin_namespace.doc(
        description = "Delete an Admin by ID - Admins Only",
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