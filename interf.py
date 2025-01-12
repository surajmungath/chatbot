import pickle
import random
import nltk
from nltk.tokenize import word_tokenize

# Ensure nltk data is downloaded
try:
    nltk.download("punkt", quiet=True)
except Exception as e:
    print(f"Warning: Could not download NLTK data: {e}")

# Keywords and their responses
KEYWORD_RESPONSES = {
    # Greetings
    "hello": ["Hi there! How can I help you today?", "Hello! What's on your mind?", "Hey! Ready to chat?"],
    "hi": ["Hi! How are you?", "Hello there! What can I do for you?", "Hey! What's up?"],
    "hey": ["Hey! What's going on?", "Hi there! Need something?", "Hello! How can I help?"],
    
    # Questions
    "how are you": ["I'm doing great! How about you?", "I'm good, thanks for asking! How are you?", "All good here! You?"],
    "what is your name": ["I'm ChatBot! Nice to meet you!", "You can call me ChatBot!", "I'm ChatBot, your friendly assistant!"],
    "who are you": ["I'm a chatbot here to help you!", "I'm your friendly AI assistant!", "I'm ChatBot, ready to help!"],
    
    # Games
    "play": ["Sure! We have Hangman, Quiz, and Math games. Which one would you like to try?", 
            "Let's play! Choose: 1) Hangman 2) Quiz 3) Math Game", 
            "Game time! Pick one: Hangman, Quiz, or Math Game"],
    "game": ["Want to play a game? We have: 1) Hangman 2) Quiz 3) Math", 
            "Ready for some fun? Choose: Hangman, Quiz, or Math Game", 
            "Let's play! Which game: Hangman, Quiz, or Math?"],
    
    # Specific Game Responses
    "hangman": ["Starting Hangman! Try to guess the word!", "Let's play Hangman! Ready to guess?", "Hangman it is! Let's begin!"],
    "quiz": ["Quiz time! Ready for some questions?", "Let's test your knowledge with a quiz!", "Starting the quiz game!"],
    "math": ["Time for some math fun!", "Let's solve some math problems!", "Ready for math challenges?"],
    
    # Emotions
    "happy": ["That's great to hear!", "Wonderful! Happiness is contagious!", "I'm glad you're happy!"],
    "sad": ["I'm sorry you're feeling sad. Want to talk about it?", "Would a game help cheer you up?", "Let me try to make you feel better!"],
    "bored": ["Let's fix that! Want to play a game?", "How about we do something fun?", "I know some great games we could play!"],
    
    # Help
    "help": ["I can help you with: 1) Playing games 2) Chatting 3) Answering questions. What do you need?",
            "Need assistance? I'm here for games, chat, and more!",
            "How can I help? We can play games or just chat!"],
    
    # Yes/No responses
    "yes": ["Great! Let's do it!", "Awesome! Shall we begin?", "Perfect! Let's get started!"],
    "no": ["No problem! What would you like to do instead?", "That's okay! We can try something else!", "Sure, we can do something else!"],
    
    # Goodbyes
    "bye": ["Goodbye! Come back soon!", "See you later! Take care!", "Bye! Have a great day!"],
    "goodbye": ["Bye! Hope to chat again soon!", "Goodbye! Come back anytime!", "See you! Have a wonderful time!"],
    
    # Account related
    "account": ["To manage your account, please visit your Account Settings page or contact support at support@example.com",
               "Need help with your account? You can: 1) Reset password 2) Update details 3) Contact support",
               "For account-related issues, please email support@example.com or call our helpline at 1-800-XXX-XXXX"],
    
    "login": ["Having trouble logging in? Try resetting your password or contact support at support@example.com",
             "To log in, please visit our login page. If you need help, contact our support team",
             "Login issues? You can: 1) Reset password 2) Contact support 3) Check our FAQ"],
    
    "password": ["To reset your password: 1) Click 'Forgot Password' 2) Enter email 3) Follow instructions sent to your email",
                "Password reset is easy! Just use the 'Forgot Password' link and follow the steps",
                "Need to change your password? Use the reset option or contact support for help"],
    
    "forgot password": ["Click the 'Forgot Password' link on the login page and follow the instructions sent to your email",
                       "I can help you reset your password. Just use the password reset option on the login page",
                       "To recover your password: 1) Click 'Forgot Password' 2) Enter email 3) Check your inbox"],
    
    "reset password": ["To reset your password, click the 'Forgot Password' link and follow the email instructions",
                      "Password reset steps: 1) Click 'Forgot Password' 2) Enter email 3) Follow email instructions",
                      "Need to reset? Use the password reset option on the login page or contact support"],
    
    "support": ["Contact our support team at: Email: navachatbot@gmail.com | Phone: 7909192967 | Live Chat",
               "Need help? Reach our support: 1) Email: navachatbot@gmail.com 2) Phone: 7909192967 3) Live chat",
               "Our support team is available 24/7. Contact: navachatbot@gmail.com or call 7909192967"],
    
    "contact": ["You can reach us at: Email: navachatbot@gmail.com | Phone:7909192967    | Live Chat",
               "Contact options: 1) Email: navachatbot@gmail.com 2) Phone: 7909192967 3) Live chat",
               "Need to reach us? Email navachatbot@gmail.com or call 7909192967"],
    
    "help account": ["For account help: 1) Email: navachatbot@gmail.com 2) Phone: 7909192967 3) Check FAQ",
                    "Account assistance available via email (navachatbot@gmail.com) or phone (7909192967)",
                    "Need account help? Contact our support team or check our FAQ section"],
    
    "create account": ["To create an account: 1) Click 'Sign Up' 2) Fill details 3) Verify email",
                      "Creating an account is easy! Just click 'Sign Up' and follow the steps",
                      "Want to join? Use the 'Sign Up' button and follow the registration process"],
    
    "delete account": ["To delete your account, please contact our support team at navachatbot@gmail.com",
                      "Account deletion requires verification. Please contact navachatbot@gmail.com",
                      "For account deletion, email navachatbot@gmail.com with your request"],
    
    "security": ["We take security seriously. Your data is encrypted and protected",
                "Your account security is our priority. Enable 2FA for extra protection",
                "For security concerns, contact our security team at navachatbot@gmail.com"],
    
    "privacy": ["Your privacy matters. Read our privacy policy at navachatbot@gmail.com/privacy",
               "We protect your data. Check our privacy policy for details",
               "Privacy concerns? Review our policy or contact navachatbot@gmail@.com"],
    
    # Default
    "default": ["I'm not sure about that. For help, contact support@gmail.com or try our FAQ",
               "Need assistance? Contact our support team at navachatbot@gmail.com",
               "Not sure about that. Email navachatbot@gmail.com or call 790912967 for help"]
}

def find_best_match(user_input):
    """Find the best matching keyword for the user input."""
    user_input = user_input.lower().strip()
    
    # Account and support related keywords
    account_keywords = ["account", "login", "password", "forgot", "reset", "support", "contact", 
                       "help", "create", "delete", "security", "privacy"]
    
    # Direct match
    for keyword in KEYWORD_RESPONSES:
        if keyword in user_input:
            return keyword
    
    # Check for account-related words
    for word in account_keywords:
        if word in user_input:
            if "password" in user_input and "forgot" in user_input:
                return "forgot password"
            if "password" in user_input and "reset" in user_input:
                return "reset password"
            if "help" in user_input and "account" in user_input:
                return "help account"
            return word
            
    # Check for game-related words
    game_words = ["play", "game", "hangman", "quiz", "math"]
    for word in game_words:
        if word in user_input:
            return word
            
    # Check for greeting words
    greetings = ["hello", "hi", "hey", "morning", "evening"]
    for word in greetings:
        if word in user_input:
            return word
    
    return "default"

def chatbot_response(user_input):
    try:
        if not user_input:
            return {"text": "Hi there! How can I help you today?"}
        
        # Find best matching keyword
        keyword = find_best_match(user_input)
        
        # Get response for the keyword
        responses = KEYWORD_RESPONSES.get(keyword, KEYWORD_RESPONSES["default"])
        response = random.choice(responses)
        
        # Add context based on keyword
        if keyword in ["play", "game", "hangman", "quiz", "math"]:
            response += " Just type the game name to start!"
        elif keyword in ["hi", "hello", "hey"]:
            response += " Want to play a game or chat?"
        elif keyword in ["help"]:
            response += " What interests you the most?"
            
        return {"text": response}
        
    except Exception as e:
        print(f"Error in chatbot_response: {e}")
        return {"text": "I'm having trouble understanding. Want to try a game instead?"}

# Example usage
if __name__ == "__main__":
    print("Chatbot is ready. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        response = chatbot_response(user_input)
        print("Bot:", response["text"])
