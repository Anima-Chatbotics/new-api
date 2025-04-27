import requests
from flask import request, jsonify
from flask_restful import Resource
from urllib.parse import urlencode, urljoin
import logging
import json
from .models import WebChatUser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatAPI(Resource):
    """API resource for handling chat interactions."""
    
    ENDPOINTS = {
        'emis': 'https://anima.emis.ge/',
        'default': 'https://animachatbotics.com/'
    }
    
    def __init__(self):
        self.max_message_length = 182
        self.max_sentence_count = 3

    def _validate_message(self, message):
        """Validate message length and complexity."""
        if len(message) >= self.max_message_length or \
           len(message.split(".")) > self.max_sentence_count or \
           len(message.split(",")) > self.max_sentence_count:
            return "ფრანჩესკოტოტი"
        return message

    def _build_api_url(self, platform, params):
        """Build the API URL with parameters."""
        base_url = self.ENDPOINTS.get(platform, self.ENDPOINTS['default'])
        endpoint = urljoin(base_url, "ka/GetFBApi/addword")
        url = f"{endpoint}?{urlencode(params)}"
        logger.info(f"Built API URL: {url}")
        return url

    def _process_response(self, response_data, user_progress):
        """Process the API response and update user progress."""
        try:
            logger.info(f"Processing response data: {response_data}")
            
            if not response_data.get("Data"):
                logger.error("No Data in response")
                return jsonify([{"type": 0, "text": "An internal error occurred"}]), 500

            data = response_data["Data"]
            user_progress.content_id = data["lastBrainPointId"]
            user_progress.save_to_db()
            
            # Process the outputs
            outputs = data["outputs"]
            if isinstance(outputs, str):
                outputs = outputs.replace('"', "¶")
            
            # Ensure proper JSON encoding of Georgian text
            response = json.dumps(outputs, ensure_ascii=False)
            logger.info(f"Processed outputs: {response}")
            
            return response, 200, {'Content-Type': 'application/json; charset=utf-8'}
            
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            return jsonify([{"type": 0, "text": "პასუხი ვერ დამუშავდა"}])

    def post(self, platform=None):
        """Handle incoming chat messages."""
        try:
            data = request.get_json(force=True)
            logger.info(f"Received message from WebChatAPI: {data}")

            # Validate required fields
            required_fields = ['userId', 'botid', 'message']
            for field in required_fields:
                if field not in data:
                    logger.error(f"Missing required field: {field}")
                    return jsonify([{"type": 0, "text": f"Missing required field: {field}"}]), 400

            user_id = data['userId']
            bot_id = data['botid']
            message = data['message']
            tone = data.get('tone', 0)

            logger.info(f"Processing message for user {user_id}, bot {bot_id}")

            # Get or create user progress
            user_progress = WebChatUser.get_user_progress(user_id, bot_id)
            logger.info(f"User progress: {user_progress.content_id}")
            
            # Validate and process message
            processed_message = self._validate_message(message)
            logger.info(f"Processed message: {processed_message}")
            
            # Prepare API request
            params = {
                'botId': str(bot_id),
                'input': processed_message,
                'tone': str(tone),
                'lastBrainPointId': str(user_progress.content_id),
                'userID': str(user_id)
            }
            
            url = self._build_api_url(platform, params)
            
            # Make API request
            logger.info(f"Making request to: {url}")
            response = requests.post(url)
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content: {response.text}")
            
            response_data = response.json()
            return self._process_response(response_data, user_progress)
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return jsonify([{"type": 0, "text": "პასუხი ვერ მოიძებნა"}])
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return jsonify([{"type": 0, "text": "An unexpected error occurred"}]), 500 