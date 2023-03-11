from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.users import User
from ..utils.blacklist import BLACKLIST
from ..utils.decorators import admin_required
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

auth_namespace = Namespace('auth', description='Namespace for Authentication')

signup_model = auth_namespace.model(
    'Signup', {
        'name': fields.String(required=True, description="Username"),
        'email': fields.String(required=True, description="User's Email"),
        'password': fields.String(required=True, description="Password")
    }
)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="User's Email"),
        'password': fields.String(required=True, description="Password")
    }
)

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'name': fields.String(required=True, description="Username"),
        'email': fields.String(required=True, description="User's email"),
        'password_hash': fields.String(required=True, description="Password")    
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
            Register a User 
        """        
        data = request.get_json()

        new_user = User(
            name = data.get('name'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token
        """
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Refresh Access Token
        """
        user = get_jwt_identity()

        access_token = create_access_token(identity=user)

        return {'access_token': access_token}, HTTPStatus.OK


@auth_namespace.route('/logout')
class Logout(Resource):
    @jwt_required(verify_type=False)
    def post(self):
        """
            Revoke Access/Refresh Token
        """
        token = get_jwt()
        jti = token["jti"]
        token_type = token["type"]
        BLACKLIST.add(jti)
        return {"message": f"{token_type.capitalize()} token successfully revoked"}, HTTPStatus.OK


@auth_namespace.route('/users')
class GetAll(Resource):

    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(
        description="Retrieve all users"
    )
    @admin_required()
    def get(self):
        """
            Retrieve all Users
        """
        users = User.query.all()

        return users, HTTPStatus.OK


@auth_namespace.route('/users/<int:user_id>')
class GetUpdateDelete(Resource):
    
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(
        description="Retrieve a user's details by ID",
        params = {
            'user_id': "The User's ID"
        }
    )
    @jwt_required()
    def get(self, user_id):
        """
            Retrieve a User's Details by ID
        """
        user = User.get_by_id(user_id)
        
        return user, HTTPStatus.OK
    
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(
        description="Update a user's details by ID",
        params = {
            'user_id': "The User's ID"
        }
    )
    @jwt_required()
    def put(self, user_id):
        """
            Update a User's Details by ID
        """
        user = User.get_by_id(user_id)
        active_user = get_jwt_identity()
        if active_user != user:
            return 

        data = auth_namespace.payload

        user.name = data['name']
        user.email = data['email']

        user.update()

        return user, HTTPStatus.OK
    
    @auth_namespace.doc(
        description='Delete a user by ID',
        params = {
            'user_id': "The User's ID"
        }
    )
    @admin_required()
    def delete(self, user_id):
        """
            Delete a User by ID
        """
        user = User.get_by_id(user_id)

        user.delete()

        return {"message": "User Successfully Deleted"}, HTTPStatus.OK