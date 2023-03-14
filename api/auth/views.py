from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.users import User
from ..utils.blacklist import BLACKLIST
from werkzeug.security import check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

auth_namespace = Namespace('auth', description='Namespace for Authentication')

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="User's Email"),
        'password': fields.String(required=True, description="User's Password")
    }
)


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