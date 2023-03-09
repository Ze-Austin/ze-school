from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.courses import Course
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


@course_namespace.route('/courses')
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
    

@course_namespace.route('/course/<int:course_id>')
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
        course = course.get_by_id(course_id)
        
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
        course = course.get_by_id(course_id)

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
        course = course.get_by_id(course_id)

        course.delete()

        return {"message": "Course Successfully Deleted"}, HTTPStatus.OK