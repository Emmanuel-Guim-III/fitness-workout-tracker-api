import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.exercise import Exercise

app = create_app()
app.app_context().push()

# Your seeding logic
exercises = [
    Exercise(name="Bench Press", description="Barbell chest press", default_sets=3, default_reps=8),
    Exercise(name="Deadlift", description="Barbell deadlift from floor", default_sets=3, default_reps=5),
    Exercise(name="Squat", description="Barbell back squat", default_sets=3, default_reps=8),
    Exercise(name="Pull-Up", description="Bodyweight pull-up", default_sets=3, default_reps=10),
    Exercise(name="Overhead Press", description="Standing barbell overhead press", default_sets=3, default_reps=8),
    Exercise(name="Bicep Curl", description="Dumbbell bicep curl", default_sets=3, default_reps=12),
    Exercise(name="Tricep Dip", description="Bodyweight tricep dip", default_sets=3, default_reps=10),
    Exercise(name="Plank", description="Static core exercise", default_sets=3, default_reps=1)
]

db.session.bulk_save_objects(exercises)
db.session.commit()

print("✅ Exercises seeded successfully.")
