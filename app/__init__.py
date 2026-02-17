from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Ensure upload folder exists (with error handling for Vercel)
    try:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except Exception as e:
        print(f"Directory creation skipped: {e}")

    # Register blueprints
    from app.auth import auth as auth_blueprint
    from app.routes import main as main_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    # Database setup
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database creation error: {e}")

    @app.route('/health')
    def health():
        return {"status": "healthy"}, 200

    return app
