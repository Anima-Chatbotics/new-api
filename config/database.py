import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'name': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'a007e7bd08e8b5d8'),
    'host': os.getenv('DB_HOST', 'srv-captain--anima-db'),
    'port': os.getenv('DB_PORT', '5432'),
    'version': os.getenv('DB_VERSION', '14.5')
}

# SQLAlchemy database URL
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['name']}" 