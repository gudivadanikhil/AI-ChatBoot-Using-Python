import streamlit as st
import json
import random
import nltk
import pickle
import os
import html
import re

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "can", "do", "for", "i",
    "in", "is", "it", "me", "of", "on", "or", "the", "to", "you", "your",
}

class AIChatbot:
    def __init__(self, intents_file='intents.json'):
        self.intents = None
        self.words = []
        self.classes = []
        self.load_intents(intents_file)
    
    def load_intents(self, intents_file):
        """Load intents from JSON file"""
        if os.path.exists(intents_file):
            with open(intents_file, 'r', encoding='utf-8') as f:
                self.intents = json.load(f)
        else:
            # Use default intents if file doesn't exist
            self.intents = self.get_default_intents()
            # Save it for next time
            with open(intents_file, 'w', encoding='utf-8') as f:
                json.dump(self.intents, f, indent=4, ensure_ascii=False)
    
    def get_default_intents(self):
        """Default intents for the chatbot"""
        return {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["hello", "hi", "hey", "good morning", "greetings", "what's up", "howdy"],
                    "responses": ["Hello! 👋", "Hi there! How can I help you?", "Hey! What's up?", "Greetings! 😊"]
                },
                {
                    "tag": "goodbye",
                    "patterns": ["bye", "goodbye", "see you", "farewell", "take care", "see you later", "see you soon"],
                    "responses": ["Goodbye! 👋", "See you later!", "Have a great day!", "Take care! 😊", "See you soon!"]
                },
                {
                    "tag": "name",
                    "patterns": ["what is your name", "who are you", "tell me your name", "your name", "call yourself"],
                    "responses": ["I'm AI Chatbot, your helpful assistant! 🤖", "I'm a friendly AI Chatbot here to help!", "You can call me AI Chatbot!"]
                },
                {
                    "tag": "help",
                    "patterns": ["help", "can you help", "i need help", "assist", "support"],
                    "responses": ["Of course! I'm here to help. What do you need? 🤝", "I'd be happy to assist! What can I do for you?", "Sure thing! How can I help?"]
                },
                {
                    "tag": "how_are_you",
                    "patterns": ["how are you", "how do you feel", "what about you", "how's it going", "how are you doing"],
                    "responses": ["I'm doing great, thanks for asking! 😊", "I'm functioning perfectly, thanks!", "All systems go! How about you?"]
                },
                {
                    "tag": "capabilities",
                    "patterns": ["what can you do", "your capabilities", "what are your features", "tell me about yourself"],
                    "responses": ["I can chat with you, answer questions, and provide helpful responses! I'm here 24/7 to assist. 🤖", "I can engage in conversation, understand your queries, and provide useful information!"]
                },
                {
                    "tag": "thanks",
                    "patterns": ["thanks", "thank you", "appreciate", "grateful", "thanks a lot"],
                    "responses": ["You're welcome! 😊", "Happy to help!", "Anytime! That's what I'm here for.", "No problem at all!"]
                },
                {
                    "tag": "time",
                    "patterns": ["what time is it", "tell me the time", "current time", "what's the time"],
                    "responses": ["I don't have access to real-time data, but you can check your device's clock! ⏰", "My apologies, I can't access the current time. Check your system clock!"]
                },
                {
                    "tag": "weather",
                    "patterns": ["how's the weather", "what's the weather", "is it raining", "weather forecast"],
                    "responses": ["I can't check the weather right now, but you can check a weather app! 🌤️", "I don't have access to weather data. Try a weather service!"]
                },
                {
                    "tag": "joke",
                    "patterns": ["tell me a joke", "make me laugh", "funny", "do you know any jokes"],
                    "responses": ["Why did the AI go to school? To improve its learning model! 😄", "Why do programmers prefer dark mode? Because light attracts bugs! 💡😄", "I tried to tell a joke about TCP, but I wasn't sure if you'd get it! 😄"]
                }
            ]
        }
    
    def preprocess(self, text):
        """Preprocess text without requiring NLTK data downloads."""
        tokens = re.findall(r"[a-z0-9']+", text.lower())
        return [w for w in tokens if w not in STOP_WORDS]
    
    def find_best_intent(self, user_input):
        """Find the best matching intent"""
        user_tokens = set(self.preprocess(user_input))
        best_match = None
        best_score = 0
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                pattern_tokens = set(self.preprocess(pattern))
                # Calculate similarity using Jaccard similarity
                if len(user_tokens) == 0 and len(pattern_tokens) == 0:
                    score = 1.0
                elif len(user_tokens) == 0 or len(pattern_tokens) == 0:
                    score = 0
                else:
                    intersection = len(user_tokens & pattern_tokens)
                    union = len(user_tokens | pattern_tokens)
                    score = intersection / union if union > 0 else 0
                
                if score > best_score:
                    best_score = score
                    best_match = intent
        
        return best_match, best_score
    
    def get_response(self, user_input):
        """Get chatbot response"""
        if not user_input.strip():
            return "Please say something! 😊"
        
        intent, confidence = self.find_best_intent(user_input)
        
        if intent and confidence > 0.3:
            response = random.choice(intent['responses'])
            return response
        else:
            default_responses = [
                "I'm not quite sure about that. Could you rephrase? 🤔",
                "That's interesting! Can you tell me more? 💭",
                "I don't have information about that, but I'm learning! 📚",
                "Hmm, I haven't learned that yet. Ask me something else! 😊"
            ]
            return random.choice(default_responses)

# Page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        justify-content: flex-end;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
    .message-content {
        max-width: 70%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = AIChatbot()

# Header
st.title("🤖 AI Chatbot")
st.markdown("---")

# Display chat history
for i, (sender, message) in enumerate(st.session_state.chat_history):
    safe_message = html.escape(message)
    if sender == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-content">
                    <p><strong>You:</strong> {safe_message}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-content">
                    <p><strong>🤖 Bot:</strong> {safe_message}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Input section
st.markdown("---")
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input("You:", placeholder="Type your message here...", key="input")

with col2:
    send_button = st.button("Send", use_container_width=True)

# Process user input
if send_button and user_input:
    # Add user message to history
    st.session_state.chat_history.append(("user", user_input))
    
    # Get bot response
    bot_response = st.session_state.chatbot.get_response(user_input)
    st.session_state.chat_history.append(("bot", bot_response))
    
    # Rerun to update display
    st.rerun()

# Footer with info
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8rem;">
    <p>💬 AI Chatbot v1.0 | Built with Python & Streamlit</p>
    <p>Type 'help' to see what I can do!</p>
</div>
""", unsafe_allow_html=True)
