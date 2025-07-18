from flask import Blueprint, request, jsonify
from app import db
from app.models.workout import Workout
from app.models.exercise import Exercise
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
workout_bp = Blueprint('workouts', __name__)

@workout_bp.route('workouts', methods=['POST'])
@jwt_required()
def create_workout():
    data = request.get_json()
    title = data.get('title')
    scheduled_date_str = data.get('scheduled_date')
    scheduled_date = datetime.fromisoformat(scheduled_date_str) if scheduled_date_str else None
    exercise_ids = data.get('exercise_ids', [])
    notes = data.get('notes', '')

    user_id = get_jwt_identity()

    workout = Workout(
        title=title,
        scheduled_date=scheduled_date,
        user_id=user_id,
        notes=notes
    )

    for ex_id in exercise_ids:
        exercise = Exercise.query.get(ex_id)
        if exercise:
            workout.exercises.append(exercise)

    db.session.add(workout)
    db.session.commit()

    return jsonify({'message': 'Workout created successfully.'}), 201
