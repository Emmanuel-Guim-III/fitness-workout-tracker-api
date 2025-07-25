from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object("config.Config")
    
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    jwt = JWTManager(app)

    db.init_app(app)

    # Register blueprints (routes)
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")

    from .routes.workouts import workout_bp
    app.register_blueprint(workout_bp, url_prefix="/api")
    
    from .routes.workout_logs import log_bp
    app.register_blueprint(log_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app