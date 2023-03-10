from ..utils import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    course = db.relationship('Course', backref='students', lazy=True)
    student = db.relationship('User', backref='students', lazy=True)

    def __repr__(self):
        return f"<Student {self.student_id}>"
        
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