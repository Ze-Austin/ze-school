from ..utils import db

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    percent_grade = db.Column(db.Float(), nullable=False)
    letter_grade = db.Column(db.String(5), nullable=True)

    def __repr__(self):
        return f"<{self.percent_grade}%>"
        
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