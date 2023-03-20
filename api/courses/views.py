from flask_restx import Namespace, Resource, fields
from ..models.courses import Course
from ..models.students import Student
from ..models.student_course import StudentCourse
from ..utils.decorators import admin_required
from http import HTTPStatus
from flask_jwt_extended import jwt_required

course_namespace = Namespace('courses', description='Namespace for Courses')

course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description="Course's ID"),
        'name': fields.String(description="Course's Name", required=True),
        'teacher': fields.String(description="Course's Teacher", required=True)
    }
)

course_student_model = course_namespace.model(
    'CourseStudent', {
        'course_id': fields.Integer(description="Course's ID"),
        'student_id': fields.Integer(description="Student's User ID")
    }
)


@course_namespace.route('')
class GetCreateCourses(Resource):

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Get All Courses"
    )
    @jwt_required()
    def get(self):
        """
            Get All Courses
        """
        courses = Course.query.all()

        return courses, HTTPStatus.OK
    
    @course_namespace.expect(course_model)
    @course_namespace.doc(
        description='Register a Course - Admins Only'
    )
    @admin_required()
    def post(self):
        """
            Register a Course - Admins Only
        """
        data = course_namespace.payload

        # Check if course already exists
        course = Course.query.filter_by(name=data['name']).first()
        if course:
            return {"message": "Course Already Exists"}, HTTPStatus.CONFLICT

        # Register new course
        new_course = Course(
            name = data['name'],
            teacher = data['teacher']
        )

        new_course.save()

        course_resp = {}
        course_resp['id'] = new_course.id
        course_resp['name'] = new_course.name
        course_resp['teacher'] = new_course.teacher

        return course_resp, HTTPStatus.CREATED
    

@course_namespace.route('/<int:course_id>')
class GetUpdateDeleteCourse(Resource):
    
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Retrieve a Course's Details by ID - Admins Only",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def get(self, course_id):
        """
            Retrieve a Course's Details by ID - Admins Only
        """
        course = Course.get_by_id(course_id)
        
        return course, HTTPStatus.OK
    
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = "Update a Course's Details by ID - Admins Only",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def put(self, course_id):
        """
            Update a Course's Details by ID - Admins Only
        """
        course = Course.get_by_id(course_id)

        data = course_namespace.payload

        course.name = data['name']
        course.teacher = data['teacher']

        course.update()

        return course, HTTPStatus.OK
    
    @course_namespace.doc(
        description = "Delete a Course by ID - Admins Only",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def delete(self, course_id):
        """
            Delete a Course by ID - Admins Only
        """
        course = Course.get_by_id(course_id)

        course.delete()

        return {"message": "Course Successfully Deleted"}, HTTPStatus.OK


@course_namespace.route('/<int:course_id>/students')
class GetAllCourseStudents(Resource):

    @course_namespace.doc(
        description = "Get All Students Enrolled for a Course - Admins Only",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def get(self, course_id):
        """
            Get All Students Enrolled for a Course - Admins Only
        """
        students = StudentCourse.get_students_in_course(course_id)
        resp = []

        for student in students:
            student_resp = {}
            student_resp['id'] = student.id
            student_resp['first_name'] = student.first_name
            student_resp['last_name'] = student.last_name
            student_resp['matric_no'] = student.matric_no

            resp.append(student_resp)

        return resp, HTTPStatus.OK


@course_namespace.route('/<int:course_id>/students/<int:student_id>')
class AddDropCourseStudent(Resource):
    
    @course_namespace.doc(
        description = "Enroll a Student for a Course - Admins Only",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @admin_required()
    def post(self, course_id, student_id):
        """
            Enroll a Student for a Course - Admins Only
        """
        course = Course.get_by_id(course_id)
        student = Student.get_by_id(student_id)
        
        student_in_course = StudentCourse.query.filter_by(
                student_id=student.id, course_id=course.id
            ).first()
        if student_in_course:
            return {
                "message": f"{student.first_name} {student.last_name} is already registered for {course.name}"
            }, HTTPStatus.OK
        
        course_student =  StudentCourse(
            course_id = course_id,
            student_id = student_id
        )

        course_student.save()

        course_student_resp = {}
        course_student_resp['course_id'] = course_student.course_id
        course_student_resp['course_name'] = course.name
        course_student_resp['course_teacher'] = course.teacher
        course_student_resp['student_id'] = course_student.student_id
        course_student_resp['student_first_name'] = student.first_name
        course_student_resp['student_last_name'] = student.last_name
        course_student_resp['student_matric_no'] = student.matric_no

        return course_student_resp, HTTPStatus.CREATED

    @course_namespace.doc(
        description = 'Remove a Student from a Course - Admins Only',
        params = {
            'course_id': "The Course's ID",
            'student_id': "The Student's ID"
        }
    )
    @admin_required()
    def delete(self, course_id, student_id):
        """
            Remove a Student from a Course - Admins Only
        """

        # Confirm existence of student and course
        course = Course.query.filter_by(id=course_id).first()
        student = Student.query.filter_by(id=student_id).first()
        if not student or not course:
            return {"message": "Student or Course Not Found"}, HTTPStatus.NOT_FOUND
        
        # Check if student is not registered for the course
        student_in_course = StudentCourse.query.filter_by(
                student_id=student.id, course_id=course.id
            ).first()
        if not student_in_course:
            return {
                "message": f"{student.first_name} {student.last_name} is not registered for {course.name}"
            }, HTTPStatus.NOT_FOUND

        # Remove the student from the course
        student_in_course.delete()

        return {"message": f"{student.first_name} {student.last_name} has been successfully removed from {course.name}"}, HTTPStatus.OK