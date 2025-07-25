from flask import Blueprint, request, jsonify
from app.models.exercise import Exercise
from app import db

exercise_bp = Blueprint('exercises', __name__)

@exercise_bp.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([{
        'id': ex.id,
        'name': ex.name,
        'description': ex.description,
        'default_sets': ex.default_sets,
        'default_reps': ex.default_reps
    } for ex in exercises]), 200

@exercise_bp.route('/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    return jsonify({
        'id': exercise.id,
        'name': exercise.name,
        'description': exercise.description,
        'default_sets': exercise.default_sets,
        'default_reps': exercise.default_reps
    }), 200

@exercise_bp.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400

    exercise = Exercise(
        name=data['name'],
        description=data.get('description'),
        default_sets=data.get('default_sets'),
        default_reps=data.get('default_reps')
    )

    db.session.add(exercise)
    db.session.commit()

    return jsonify({'message': 'Exercise created', 'id': exercise.id}), 201

@exercise_bp.route('/exercises/<int:exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    data = request.get_json()

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    exercise.name = data.get('name', exercise.name)
    exercise.description = data.get('description', exercise.description)
    exercise.default_sets = data.get('default_sets', exercise.default_sets)
    exercise.default_reps = data.get('default_reps', exercise.default_reps)

    db.session.commit()
    return jsonify({'message': 'Exercise updated'}), 200

@exercise_bp.route('/exercises/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)

    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted'}), 200
