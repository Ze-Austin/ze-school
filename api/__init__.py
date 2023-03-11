from flask import Flask
from flask_restx import Api
from dotenv import load_dotenv
from .auth.views import auth_namespace
from .courses.views import course_namespace
from .config.config import config_dict
from .utils import db
from .utils.blacklist import BLACKLIST
from .models.users import User
from .models.courses import Course
from .models.students import Student
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed
from http import HTTPStatus

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    load_dotenv()

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    # Make the first registered user an admin
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {
                'is_admin': True
            }
        else:
            return {
                'is_admin': False
            }
    

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLACKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has been revoked",
            "error": "token_revoked"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.expired_token_loader
    def expired_token_callback():
        return {
            "message": "The token has expired",
            "error": "token_expired"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Token verification failed",
            "error": "invalid_token"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Request is missing an access token",
            "error": "authorization_required"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return {
            "message": "The token is not fresh",
            "error": "fresh_token_required"
        }, HTTPStatus.UNAUTHORIZED

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }

    api = Api(
        app,
        title='Student Management API',
        description='A student management REST API service',
        authorizations=authorizations,
        security='Bearer Auth'
        )

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(course_namespace, path='/courses')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, HTTPStatus.NOT_FOUND

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Course': Course,
            'Student': Student
        }

    return app