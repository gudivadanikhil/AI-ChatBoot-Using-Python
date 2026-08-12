"""
ADVANCED AI CHATBOT with TensorFlow Neural Network

This is an enhanced version that uses deep learning for better accuracy.
Requires: tensorflow, numpy

Install: pip install tensorflow numpy

Usage:
    python chatbot_advanced.py
"""

import json
import random
import nltk
import numpy as np
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import tensorflow as tf
    from tensorflow import keras
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False
    print("⚠️  TensorFlow not installed!")
    print("Install it with: pip install tensorflow")

class NeuralChatbot:
    def __init__(self, intents_file='intents.json'):
        self.words = []
        self.classes = []
        self.intents = self.load_intents(intents_file)
        self.model = None
        
        if HAS_TENSORFLOW:
            self._prepare_training_data()
            self._build_model()
            print("✅ Neural network model created!")
    
    def load_intents(self, intents_file):
        """Load intents from JSON"""
        if os.path.exists(intents_file):
            with open(intents_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self.get_default_intents()
    
    def get_default_intents(self):
        """Default intents"""
        return {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["hello", "hi", "hey", "good morning", "greetings"],
                    "responses": ["Hello! 👋", "Hi there!", "Hey! How can I help?"]
                },
                {
                    "tag": "goodbye",
                    "patterns": ["bye", "goodbye", "see you", "farewell"],
                    "responses": ["Goodbye! 👋", "See you later!", "Have a great day!"]
                },
                {
                    "tag": "thanks",
                    "patterns": ["thanks", "thank you", "appreciate", "grateful"],
                    "responses": ["You're welcome! 😊", "Happy to help!", "No problem!"]
                },
                {
                    "tag": "joke",
                    "patterns": ["tell me a joke", "make me laugh", "funny"],
                    "responses": ["Why do programmers prefer dark mode? Light attracts bugs! 😄"]
                }
            ]
        }
    
    def _prepare_training_data(self):
        """Prepare data for neural network"""
        print("📚 Preparing training data...")
        
        # Collect all words and classes
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                tokens = self._tokenize(pattern)
                self.words.extend(tokens)
            
            if intent['tag'] not in self.classes:
                self.classes.append(intent['tag'])
        
        # Lemmatize and deduplicate
        self.words = sorted(set(self.words))
        self.classes = sorted(self.classes)
        
        print(f"   Found {len(self.words)} unique words")
        print(f"   Found {len(self.classes)} intent classes")
    
    def _build_model(self):
        """Build and train neural network"""
        print("🧠 Building neural network...")
        
        # Prepare training data
        X_train = []
        y_train = []
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                # Create bag of words
                bag = self._vectorize_pattern(pattern)
                X_train.append(bag)
                
                # One-hot encode the label
                label = [0] * len(self.classes)
                label[self.classes.index(intent['tag'])] = 1
                y_train.append(label)
        
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        # Build neural network
        self.model = keras.Sequential([
            keras.layers.Dense(128, input_shape=(len(self.words),), activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(len(self.classes), activation='softmax')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Train the model
        print("🔄 Training model (this may take a moment)...")
        self.model.fit(
            X_train, y_train,
            epochs=200,
            batch_size=5,
            verbose=0
        )
        print("✅ Model trained!")
    
    def _vectorize_pattern(self, pattern):
        """Convert pattern to bag of words vector"""
        tokens = self._tokenize(pattern)
        
        bag = np.zeros(len(self.words))
        for token in tokens:
            if token in self.words:
                idx = self.words.index(token)
                bag[idx] = 1
        
        return bag

    def _tokenize(self, text):
        """Tokenize text without requiring NLTK data downloads."""
        return re.findall(r"[a-z0-9']+", text.lower())
    
    def get_response(self, user_input):
        """Get response using neural network"""
        if not HAS_TENSORFLOW or self.model is None:
            return self._get_fallback_response(user_input)
        
        if not user_input.strip():
            return "Please say something! 😊"
        
        # Vectorize input
        bag = self._vectorize_pattern(user_input)
        bag = np.array([bag])
        
        # Predict
        prediction = self.model.predict(bag, verbose=0)[0]
        predicted_class_idx = np.argmax(prediction)
        confidence = prediction[predicted_class_idx]
        
        if confidence > 0.5:
            predicted_tag = self.classes[predicted_class_idx]
            for intent in self.intents['intents']:
                if intent['tag'] == predicted_tag:
                    response = random.choice(intent['responses'])
                    return f"{response} (Confidence: {confidence:.1%})"
        
        return self._get_fallback_response(user_input)
    
    def _get_fallback_response(self, user_input):
        """Fallback when model not available or confidence is low"""
        responses = [
            "I'm not sure about that. 🤔",
            "Can you rephrase that? 💭",
            "Tell me more! 📚",
            "That's interesting! 😊"
        ]
        return random.choice(responses)

def print_banner():
    """Print banner"""
    if HAS_TENSORFLOW:
        print("\n" + "="*50)
        print("🤖 AI CHATBOT - ADVANCED (TensorFlow)")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("🤖 AI CHATBOT - BASIC (TensorFlow not available)")
        print("="*50)
    print("Type 'quit' to exit | Type 'help' for commands")
    print("="*50 + "\n")

def main():
    """Main chat loop"""
    print_banner()
    bot = NeuralChatbot()
    
    print("Ready! Start chatting!\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🤖 Bot: Goodbye! 👋\n")
                break
            
            response = bot.get_response(user_input)
            print(f"🤖 Bot: {response}\n")
            
        except KeyboardInterrupt:
            print("\n🤖 Bot: See you! 👋\n")
            break

if __name__ == "__main__":
    main()
