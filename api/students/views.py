from flask_restx import Namespace, Resource, fields
from ..models.students import Student
from ..utils.decorators import admin_required
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

student_namespace = Namespace('students', description='Namespace for Students')

student_signup_model = student_namespace.model(
    'StudentSignup', {
        'first_name': fields.String(required=True, description="Student's First Name"),
        'last_name': fields.String(required=True, description="Students's Last Name"),
        'email': fields.String(required=True, description="Student's Email"),
        'password': fields.String(required=True, description="Student's Temporary Password"),
        'matric_no': fields.String(required=True, description="Student's Matriculation Number")
    }
)

student_model = student_namespace.model(
    'Student', {
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="Student's Email"),
        'password_hash': fields.String(required=True, description="Student's Password"),
        'user_type': fields.String(required=True, description="Type of student"),
        'matric_no': fields.String(required=True, description="Student's Matriculation Number")    
    }
)


@student_namespace.route('')
class GetAllStudents(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Retrieve all students"
    )
    @admin_required()
    def get(self):
        """
            Retrieve all Students - Admins Only
        """
        students = Student.query.all()

        return students, HTTPStatus.OK


@student_namespace.route('/register')
class StudentRegistration(Resource):

    @student_namespace.expect(student_signup_model)
    @student_namespace.marshal_with(student_model)
    @admin_required()
    def post(self):
        """
            Register a Student - Admins Only
        """        
        data = student_namespace.payload

        new_student = Student(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            matric_no = data['matric_no'],
            user_type = 'student'
        )

        new_student.save()

        return new_student, HTTPStatus.CREATED


@student_namespace.route('/<int:student_id>')
class GetUpdateDeleteStudents(Resource):
    
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Retrieve a student's details by ID",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Retrieve a Student's Details by ID
        """
        student = Student.get_by_id(student_id)
        
        return student, HTTPStatus.OK
    
    @student_namespace.expect(student_signup_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Update a student's details by ID",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    def put(self, student_id):
        """
            Update a Student's Details by ID
        """
        student = Student.get_by_id(student_id)
        active_student = get_jwt_identity()
        if active_student != student:
            return 

        data = student_namespace.payload

        student.first_name = data['name']
        student.last_name = data['name']
        student.email = data['email']
        student.password_hash = generate_password_hash(data['password'])

        student.update()

        return student, HTTPStatus.OK
    
    @student_namespace.doc(
        description='Delete a student by ID',
        params = {
            'student_id': "The Student's ID"
        }
    )
    @admin_required()
    def delete(self, student_id):
        """
            Delete a student by ID - Admins Only
        """
        student = Student.get_by_id(student_id)

        student.delete()

        return {"message": "Student Successfully Deleted"}, HTTPStatus.OK