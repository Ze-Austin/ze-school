from .users import User
from ..utils import db

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    matric_no = db.Column(db.String(30), unique=True)
    course = db.relationship('Course', secondary='student_course', lazy=True)
    grade = db.relationship('Grade', backref='student_grade', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __repr__(self):
        return f"<Student {self.matric_no}>"
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)