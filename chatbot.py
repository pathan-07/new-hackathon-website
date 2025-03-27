import os
import logging
import google.generativeai as genai
from flask import Blueprint, jsonify, request, session
from dotenv import load_dotenv

chatbot = Blueprint('chatbot', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load gemini api
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.warning("Gemini API key not found!")

try:
    genai.configure(api_key=API_KEY)
    # Set up the model with more parameters
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
    
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    logger.info("Gemini API initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini API: {str(e)}")
    model = None

# Initialize chat history
def get_chat_history():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return session['chat_history']

@chatbot.route('/api/chat', methods=['POST'])
def chat():
    if not model:
        return jsonify({'error': 'Gemini API not properly configured'}), 500
        
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
            
        user_message = data['message']
        chat_history = get_chat_history()
        
        # Instead of storing the conversation object in the session, 
        # create a new conversation each time with the history
        history = []
        for msg in chat_history:
            if msg["role"] == "user":
                history.append({"role": "user", "parts": [msg["content"]]})
            else:
                history.append({"role": "model", "parts": [msg["content"]]})
        
        # Create a new conversation each time
        convo = model.start_chat(history=history)
        
        # Generate response
        response = convo.send_message(user_message)
        
        # Update chat history in session
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": response.text})
        session['chat_history'] = chat_history[-10:]  # Keep only last 10 messages
        
        return jsonify({
            'response': response.text,
            'history': chat_history
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'details': str(e)}
        ), 500

@chatbot.route('/api/reset-chat', methods=['POST'])
def reset_chat():
    try:
        if 'chat_history' in session:
            session.pop('chat_history')
        return jsonify({'message': 'Chat history reset successfully'})
    except Exception as e:
        logger.error(f"Error resetting chat: {str(e)}")
        return jsonify({'error': str(e)}), 500
