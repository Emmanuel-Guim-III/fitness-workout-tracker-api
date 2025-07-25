from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.workout_log import WorkoutLog
from app.models.workout import Workout
from app.models.exercise import Exercise

log_bp = Blueprint('workout_logs', __name__)

@log_bp.route('/workout-logs', methods=['POST'])
@jwt_required()
def create_log():
    data = request.get_json()
    user_id = get_jwt_identity()

    workout = Workout.query.filter_by(id=data['workout_id'], user_id=user_id).first()
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    exercise = Exercise.query.get(data['exercise_id'])
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    log = WorkoutLog(
        workout_id=workout.id,
        exercise_id=exercise.id,
        sets=data['sets'],
        reps=data['reps'],
        weight=data.get('weight')
    )

    db.session.add(log)
    db.session.commit()
    
    return jsonify({"message": "Workout log created", "log_id": log.id}), 201

@log_bp.route('/workouts/<int:workout_id>/logs', methods=['GET'])
@jwt_required()
def get_workout_logs(workout_id):
    user_id = get_jwt_identity()
    
    # Ensure the workout belongs to the current user
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()
    if not workout:
        return jsonify({"error": "Workout not found or unauthorized"}), 404

    logs = WorkoutLog.query.filter_by(workout_id=workout_id).all()

    result = []
    for log in logs:
        result.append({
            'id': log.id,
            'timestamp': log.timestamp.isoformat(),
            'sets': log.sets,
            'reps': log.reps,
            'weight': log.weight,
        })

    return jsonify(result), 200

@log_bp.route('/workout-logs/<int:log_id>', methods=['PUT'])
@jwt_required()
def update_log(log_id):
    data = request.get_json()

    log = WorkoutLog.query.filter_by(id=log_id).first()
    if not log:
        return jsonify({"error": "Log not found"}), 404

    # Update fields
    log.sets = data.get('sets', log.sets)
    log.reps = data.get('reps', log.reps)
    log.weight = data.get('weight', log.weight)

    db.session.commit()
    return jsonify({"message": "Workout log updated"}), 200

@log_bp.route('/workout-logs/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_log(log_id):
    log = WorkoutLog.query.filter_by(id=log_id).first()
    if not log:
        return jsonify({"error": "Workout log not found"}), 404

    db.session.delete(log)
    db.session.commit()

    return jsonify({"message": "Workout log deleted"}), 200
