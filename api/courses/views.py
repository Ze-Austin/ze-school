from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.courses import Course
from ..models.students import Student
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request
from functools import wraps

course_namespace = Namespace('courses', description='Namespace for Courses')

course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description="Course's ID"),
        'name': fields.String(description="Course's Name", required=True),
        'teacher': fields.String(description="Teacher taking the Course", required=True)
    }
)

student_model = course_namespace.model(
    'Student', {
        'course_id': fields.Integer(description="Course's ID"),
        'student_id': fields.Integer(description="Student's User ID")
    }
)

# Custom decorator to verify admin access
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return {"message": "Administrator access required"}, HTTPStatus.FORBIDDEN
        return decorator
    return wrapper


@course_namespace.route('')
class GetCreate(Resource):

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Get all courses'
    )
    @jwt_required()
    def get(self):
        """
            Get All Courses
        """
        courses = Course.query.all()

        return courses, HTTPStatus.OK
    
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Register a course'
    )
    @admin_required()
    def post(self):
        """
            Register a Course
        """
        data = course_namespace.payload

        new_course = Course(
            name = data['name'],
            teacher = data['teacher']
        )

        new_course.save()

        return new_course, HTTPStatus.CREATED
    

@course_namespace.route('/<int:course_id>')
class GetUpdateDelete(Resource):
    
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description="Retrieve a course's details by ID",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def get(self, course_id):
        """
            Retrieve a Course's Details by ID
        """
        course = Course.get_by_id(course_id)
        
        return course, HTTPStatus.OK
    
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description="Update a course's details by ID",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def put(self, course_id):
        """
            Update a Course's Details by ID
        """
        course = Course.get_by_id(course_id)

        data = course_namespace.payload

        course.name = data['name']
        course.email = data['email']

        course.update()

        return course, HTTPStatus.OK
    
    @course_namespace.doc(
        description='Delete a course by ID',
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def delete(self, course_id):
        """
            Delete a course by ID
        """
        course = Course.get_by_id(course_id)

        course.delete()

        return {"message": "Course Successfully Deleted"}, HTTPStatus.OK


@course_namespace.route('/<int:course_id>/students')
class StudentEnrollment(Resource):

    @course_namespace.marshal_with(student_model)
    @course_namespace.doc(
        description="Get all students enrolled for a course",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def get(self, course_id):
        """
            Get all Students enrolled for a Course
        """
        course = Course.get_by_id(course_id)

        students = course.students

        return students, HTTPStatus.OK
    
    @course_namespace.expect(student_model)
    @course_namespace.marshal_with(student_model)
    @course_namespace.doc(
        description="Enroll students for a course",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def post(self, course_id):
        """
            Enroll Students for a Course
        """
        data = course_namespace.payload

        enrolled_student =  Student(
            course_id = course_id,
            student_id = data['student_id']
        )

        enrolled_student.save()

        return enrolled_student, HTTPStatus.CREATED