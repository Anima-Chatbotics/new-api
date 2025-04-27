from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from . import db

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Configure database
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Fallback to SQLite for local development
        database_url = 'sqlite:///chat.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from .routes import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 