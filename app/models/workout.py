from app import db
from datetime import datetime

# Association table (many-to-many between workouts and exercises)
workout_exercises = db.Table(
    'workout_exercises',
    db.Column('workout_id', db.Integer, db.ForeignKey('workouts.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercises.id'), primary_key=True)
)

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_done = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='workouts')

    exercises = db.relationship('Exercise', secondary=workout_exercises, backref='workouts')

    def __repr__(self):
        return f"<Workout {self.title} on {self.scheduled_date}>"
