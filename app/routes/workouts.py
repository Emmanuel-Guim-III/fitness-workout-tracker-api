from flask import Blueprint, request, jsonify
from app import db
from app.models.workout import Workout
from app.models.exercise import Exercise
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
workout_bp = Blueprint('workouts', __name__)

@workout_bp.route('/workouts', methods=['POST'])
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

@workout_bp.route('/workouts', methods=['GET'])
@jwt_required()
def get_all_workouts():
    user_id = get_jwt_identity()
    workouts = Workout.query.filter_by(user_id=user_id).order_by(Workout.scheduled_date.asc()).all()

    result = []
    for workout in workouts:
        result.append({
            'id': workout.id,
            'title': workout.title,
            'scheduled_date': workout.scheduled_date.isoformat(),
            'is_done': workout.is_done,
            'notes': workout.notes,
            'exercise_ids': [e.id for e in workout.exercises]
        })

    return jsonify(result), 200

@workout_bp.route('/workouts/<int:workout_id>', methods=['PUT'])
@jwt_required()
def update_workout(workout_id):
    user_id = get_jwt_identity()
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()

    if not workout:
        return jsonify({'error': 'Workout not found'}), 404

    data = request.get_json()
    workout.title = data.get('title', workout.title)
    workout.notes = data.get('notes', workout.notes)
    workout.is_done = data.get('is_done', workout.is_done)

    # Update scheduled_date if provided
    if 'scheduled_date' in data:
        try:
            workout.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
        except ValueError:
            return jsonify({'error': 'Invalid scheduled_date format'}), 400

    # Update exercises if provided
    if 'exercise_ids' in data:
        workout.exercises = []  
        for ex_id in data['exercise_ids']:
            exercise = Exercise.query.get(ex_id)
            if exercise:
                workout.exercises.append(exercise)

    db.session.commit()
    return jsonify({'message': 'Workout updated successfully'}), 200

@workout_bp.route('/workouts/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    user_id = get_jwt_identity()
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()

    if not workout:
        return jsonify({'error': 'Workout not found'}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout deleted successfully'}), 200
