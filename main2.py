from interf import chatbot_response
from game import algebra_practice_game, hangman_game, question_game
from inference import generate, model as story_model
from sentimentinf import predict_emotion, show_song, tokenizer, model as emotion_model, max_length, label_encoder
import os
import random
import nltk
from nltk.tokenize import word_tokenize

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
except Exception as e:
    print(f"Warning: Could not download NLTK data: {e}")

def identify_intent(sentence):
    """
    Identify the intent from user input based on keywords
    """
    if not isinstance(sentence, str):
        return "none"
        
    # Convert to lowercase and tokenize
    sentence = sentence.lower().strip()
    
    # Print for debugging
    print(f"\nProcessing input: '{sentence}'")
    
    # Check for direct game number inputs (1, 2, 3)
    if sentence in ['1', '2', '3']:
        print("Detected game intent (number input)")
        return "game"
    
    # Simple direct keyword matching
    if any(word in sentence for word in ['game', 'play game', 'gaming']):
        print("Detected game intent")
        return "game"
        
    if any(word in sentence for word in ['story', 'tell story', 'tell me story', 'generate story', 'write story']):
        print("Detected story intent")
        return "story"
        
    if any(word in sentence for word in ['music', 'song', 'play song', 'suggest song', 'recommend music']):
        print("Detected music intent")
        return "music"
    
    # If no specific intent is found, return none
    print("No specific intent detected")
    return "none"

def handle_game_intent(initial_input=None):
    game_options = """
Which game would you like to play?
1. Algebra - Practice math problems
2. Hangman - Guess the word
3. Quiz - Test your knowledge
(You can enter either the number or name)
"""
    if initial_input is None:
        print("\nChatbot:", game_options)
        game_choice = input("You: ").strip().lower()
    else:
        game_choice = initial_input

    # Define game mappings
    game_mappings = {
        "1": "algebra", "algebra": "algebra",
        "2": "hangman", "hangman": "hangman",
        "3": "quiz", "question": "quiz", "quiz": "quiz"
    }

    # Check if the input matches any game choice
    game_words = game_choice.split()
    selected_game = None
    
    for word in game_words:
        # Check for exact matches in game_mappings
        if word in game_mappings:
            selected_game = game_mappings[word]
            break
        # Check for numbers without quotes
        try:
            num = str(int(word))  # Convert to int and back to str to handle cases like "1.0" or "01"
            if num in game_mappings:
                selected_game = game_mappings[num]
                break
        except ValueError:
            continue

    if selected_game == "algebra":
        print("Chatbot: Starting Algebra Practice Game...")
        algebra_practice_game()
        return "I hope you enjoyed the Algebra Practice Game!"
    elif selected_game == "hangman":
        print("Chatbot: Starting Hangman Game...")
        hangman_game()
        return "I hope you had fun with Hangman!"
    elif selected_game == "quiz":
        print("Chatbot: Starting Quiz Game...")
        question_game()
        return "I hope you enjoyed the Quiz Game!"
    else:
        return "I'm not sure which game you want. Please choose a number (1-3) or name (algebra, hangman, quiz)!"

def handle_story_intent():
    if story_model is None:
        return "Sorry, the story generation model is not available at the moment."
        
    print("\nStarting story generation...")
    print("What should the story be about? (Press Enter for a random story)")
    story_prompt = input("You: ").strip()
    
    if not story_prompt:
        story_prompts = [
            "Once upon a time in a magical forest",
            "In a distant future on a space station",
            "Deep in the heart of a bustling city",
            "On a mysterious island in the middle of nowhere",
            "In an ancient castle during medieval times"
        ]
        story_prompt = random.choice(story_prompts)
        print(f"Using random prompt: {story_prompt}")
    
    try:
        print("Generating your story...")
        story = generate(story_model, start_str=story_prompt, predict_len=500)
        return f"Here's your story based on '{story_prompt}':\n\n{story}"
    except Exception as e:
        print(f"Error generating story: {e}")
        return "Sorry, I encountered an error while generating the story. Please try again."

def handle_music_intent():
    if emotion_model is None or tokenizer is None:
        return "Sorry, the music recommendation system is not available at the moment."
        
    print("\nStarting music recommendation...")
    print("How are you feeling? (happy, sad, energetic, calm, etc.)")
    music_preference = input("You: ").strip()
    
    if not music_preference:
        return "Please tell me your mood so I can recommend the perfect music!"
    
    try:
        print("Analyzing your mood....")
        emotion = predict_emotion(music_preference, tokenizer, emotion_model, max_length, label_encoder)
        song_link = show_song(emotion)
        return f"Based on your mood, I sense you're feeling {emotion}. Here's a song that matches your vibe: {song_link}"
    except Exception as e:
        print(f"Error recommending music: {e}")
        return "Sorry, I encountered an error while processing your music request. Please try again."

def process_user_input(user_input):
    """
    Process user input and redirect to appropriate model
    """
    try:
        # Check for direct game number inputs
        if user_input.strip() in ['1', '2', '3']:
            return handle_game_intent(user_input.strip())
            
        # First try to identify specific intents
        intent = identify_intent(user_input)
        print(f"Detected intent: {intent}")
        
        if intent == "game":
            return handle_game_intent(user_input)
        elif intent == "story":
            return handle_story_intent()
        elif intent == "music":
            return handle_music_intent()
            
        # If no specific intent is found, use the chatbot response
        response = chatbot_response(user_input)
        if response == "I'm having trouble processing that right now. Could you try again?":
            return "I'm not sure what you want to do. You can ask me to:\n1. Play a game\n2. Tell a story\n3. Suggest music\nOr just chat with me!"
        return response
        
    except Exception as e:
        print(f"Error processing input: {e}")
        return "I'm not sure what you want to do. You can ask me to:\n1. Play a game\n2. Tell a story\n3. Suggest music\nOr just chat with me!"

def main():
    """
    Main function to run the chatbot.
    """
    print("\n=== Chatbot is ready! Type 'quit' to exit. ===")
    print("\nYou can try:")
    print("1. Games  - Example: 'I want to play a game' or 'Let's play a game'")
    print("2. Stories - Example: 'Tell me a story' or 'Can you generate a story?'")
    print("3. Music  - Example: 'Suggest some music' or 'Can you play a song?'")
    print("Or just chat with me normally!\n")
    
    try:
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    print("Please say something!")
                    continue
                    
                if user_input.lower() == 'quit':
                    print("Goodbye! Have a great day!")
                    break
                
                response = process_user_input(user_input)
                print("\nChatbot:", response)
                
            except EOFError:
                print("\nGoodbye! Chat session ended.")
                break
            except KeyboardInterrupt:
                print("\nGoodbye! Chat session interrupted.")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                print("Please try again.")
                continue
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        print("Chatbot session terminated.")

if __name__ == "__main__":
    main()