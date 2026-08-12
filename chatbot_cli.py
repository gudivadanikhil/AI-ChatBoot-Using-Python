"""
Simple CLI AI Chatbot - Run this for a terminal-based chatbot
No Streamlit required! Perfect for testing and learning.

Usage:
    python chatbot_cli.py
"""

import json
import random
import nltk
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "can", "do", "for", "i",
    "in", "is", "it", "me", "of", "on", "or", "the", "to", "you", "your",
}

class SimpleChatbot:
    def __init__(self, intents_file='intents.json'):
        self.intents = self.load_intents(intents_file)
    
    def load_intents(self, intents_file):
        """Load intents from JSON file"""
        if os.path.exists(intents_file):
            with open(intents_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("⚠️  intents.json not found! Using default intents...")
            return self.get_default_intents()
    
    def get_default_intents(self):
        """Default intents"""
        return {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["hello", "hi", "hey", "good morning"],
                    "responses": ["Hello! 👋", "Hi there!", "Hey! What's up?"]
                },
                {
                    "tag": "goodbye",
                    "patterns": ["bye", "goodbye", "see you", "farewell"],
                    "responses": ["Goodbye! 👋", "See you later!", "Take care!"]
                },
                {
                    "tag": "name",
                    "patterns": ["what is your name", "who are you"],
                    "responses": ["I'm AI Chatbot! 🤖", "Call me ChatBot!"]
                },
                {
                    "tag": "help",
                    "patterns": ["help", "can you help"],
                    "responses": ["Of course! What do you need? 🤝", "I'm here to help!"]
                },
                {
                    "tag": "joke",
                    "patterns": ["tell me a joke", "make me laugh"],
                    "responses": ["Why do programmers prefer dark mode? Because light attracts bugs! 😄"]
                }
            ]
        }
    
    def preprocess(self, text):
        """Tokenize and remove common words without requiring NLTK data downloads."""
        tokens = re.findall(r"[a-z0-9']+", text.lower())
        return [w for w in tokens if w not in STOP_WORDS]
    
    def calculate_similarity(self, user_tokens, pattern_tokens):
        """Jaccard similarity between two token sets"""
        if not user_tokens or not pattern_tokens:
            return 0
        intersection = len(set(user_tokens) & set(pattern_tokens))
        union = len(set(user_tokens) | set(pattern_tokens))
        return intersection / union if union > 0 else 0
    
    def find_intent(self, user_input):
        """Find best matching intent"""
        user_tokens = self.preprocess(user_input)
        best_intent = None
        best_score = 0
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                pattern_tokens = self.preprocess(pattern)
                score = self.calculate_similarity(user_tokens, pattern_tokens)
                
                if score > best_score:
                    best_score = score
                    best_intent = intent
        
        return best_intent, best_score
    
    def respond(self, user_input):
        """Get response from chatbot"""
        if not user_input.strip():
            return "Please say something! 😊"
        
        intent, confidence = self.find_intent(user_input)
        
        if intent and confidence > 0.3:
            return random.choice(intent['responses'])
        else:
            defaults = [
                "Hmm, I'm not sure about that. 🤔",
                "That's interesting! Tell me more? 💭",
                "I haven't learned that yet! 📚",
                "Ask me something else! 😊"
            ]
            return random.choice(defaults)

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*50)
    print("🤖 AI CHATBOT - CLI VERSION")
    print("="*50)
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'help' to see what I can do")
    print("="*50 + "\n")

def main():
    """Main chat loop"""
    # Initialize
    print_banner()
    bot = SimpleChatbot()
    
    conversation_count = 0
    
    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            # Exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print(f"🤖 Bot: Goodbye! Thanks for chatting with me! 👋\n")
                break
            
            # Empty input
            if not user_input:
                continue
            
            # Get response
            response = bot.respond(user_input)
            print(f"🤖 Bot: {response}\n")
            conversation_count += 1
            
        except KeyboardInterrupt:
            print("\n🤖 Bot: Bye! Thanks for the conversation! 👋\n")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Let's try again!\n")
    
    # Summary
    print(f"Chat Summary: {conversation_count} messages exchanged! 😊")

if __name__ == "__main__":
    main()
