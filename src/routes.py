from flask import Blueprint, request, jsonify
from flask_restful import Api
from .models import ChatMessage
from .chat_api import ChatAPI
from . import db

chat_bp = Blueprint('chat', __name__)
api = Api(chat_bp)

# Register the ChatAPI resource
api.add_resource(ChatAPI, '/webchat/<platform>', '/webchat')

@chat_bp.route('/message', methods=['POST'])
def send_message():
    """Handle incoming chat messages."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
            
        # Create new chat message
        new_message = ChatMessage(
            content=data['message'],
            user_id=data.get('user_id', 'anonymous'),
            session_id=data.get('session_id')
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        # Here you would typically call your chatbot backend
        # For now, we'll just echo the message
        response = {
            'message': data['message'],
            'timestamp': new_message.timestamp.isoformat(),
            'message_id': new_message.id
        }
        
        return jsonify(response), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """Retrieve chat history for a specific session."""
    try:
        messages = ChatMessage.query.filter_by(session_id=session_id)\
            .order_by(ChatMessage.timestamp.asc())\
            .all()
            
        history = [{
            'id': msg.id,
            'content': msg.content,
            'user_id': msg.user_id,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]
        
        return jsonify(history), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 