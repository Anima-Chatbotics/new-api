from flask import Flask, make_response
from flask_cors import CORS
import os
from dotenv import load_dotenv
from . import db

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS with specific configuration
    CORS(app, resources={
        r"*": {
            "origins": ["https://animachatbotics.com"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True
        }
    })
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'https://animachatbotics.com')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        return response
    
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
    app.register_blueprint(chat_bp, url_prefix='WCAPI')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 