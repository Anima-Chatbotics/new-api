from . import db
from datetime import datetime

class ChatMessage(db.Model):
    """Model for storing chat messages."""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    session_id = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatMessage {self.id}>'

class WebChatUser(db.Model):
    """Model for tracking user progress in web chat."""
    __tablename__ = "webchat_progress"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    content_id = db.Column(db.Integer, default=0)
    bot_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_user_bot', 'user_id', 'bot_id'),
    )

    def __init__(self, user_id, content_id, bot_id):
        self.user_id = user_id
        self.content_id = content_id
        self.bot_id = bot_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user_progress(cls, user_id, bot_id):
        """Get or create user progress for a specific bot."""
        user_progress = cls.query.filter_by(user_id=user_id, bot_id=bot_id).first()

        if user_progress is None:
            user_progress = cls(user_id=user_id, content_id=0, bot_id=bot_id)
            user_progress.save_to_db()

        return user_progress 