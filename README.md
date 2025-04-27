# Chat API

A Flask-based API for handling Web Chat UI to Chatbot backend communication.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/chat_db
FLASK_APP=src.app:create_app()
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
HOST=0.0.0.0
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Application

Development:
```bash
flask run
```

Production:
```bash
gunicorn src.app:create_app()
```

## API Endpoints

### Send Message
- **POST** `/api/chat/message`
- Body:
```json
{
    "message": "Hello!",
    "user_id": "user123",
    "session_id": "session123"
}
```

### Get Chat History
- **GET** `/api/chat/history/<session_id>`

## Deployment on DigitalOcean with CapRover

1. Create a new app in CapRover
2. Set up the following environment variables in CapRover:
   - `DATABASE_URL`
   - `FLASK_APP`
   - `FLASK_ENV=production`
   - `FLASK_DEBUG=0`

3. Deploy using CapRover's deployment interface

## Database Setup on DigitalOcean

1. Create a new PostgreSQL database on DigitalOcean
2. Update the `DATABASE_URL` in your environment variables with the new database credentials
3. Run database migrations after deployment 