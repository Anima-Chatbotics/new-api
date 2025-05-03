from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from . import db

# Load environment variables
load_dotenv()
CORS_HEADERS = 'Content-Type, Authorization, Origin, x-csrf-token', ''
CORS_METHODS = 'GET, HEAD, POST, PATCH, DELETE, OPTIONS' 

def create_app():
    """Create and configure the Flask applicatio
    n."""
    app = Flask(__name__)
    
    # Enable CORS with specific configuration
    app.url_map.strict_slashes = False
    CORS_HEADERS = 'Content-Type, Authorization, Origin, x-csrf-token' 
    CORS(app, resources=r'/*', methods=CORS_METHODS, headers=CORS_HEADERS)
    
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