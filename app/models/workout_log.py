from app import db
from datetime import datetime

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'

    id = db.Column(db.Integer, primary_key=True)
    workout_id =db.Column(
        db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    workout = db.relationship('Workout', backref='logs')
    exercise = db.relationship('Exercise')

    def to_dict(self):
        return {
            "exercise": self.exercise.name,
            "sets": self.sets,
            "reps": self.reps,
            "weight": self.weight,
            "timestamp": self.timestamp.isoformat()
        }