from app import db

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    default_sets = db.Column(db.Integer)
    default_reps = db.Column(db.Integer)

    def __repr__(self):
        return f"<Exercise {self.name}>"
