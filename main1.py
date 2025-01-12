# from flask import Flask, render_template, request, jsonify
# from interf import chatbot_response
# from game import algebra_practice_game, hangman_game, question_game
# from inference import generate, model as story_model
# from sentimentinf import predict_emotion, show_song, tokenizer, model as emotion_model, max_length, label_encoder

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('chat.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_message = request.json.get('message', '').strip().lower()
    
#     if "game" in user_message:
#         # Define game mappings
#         game_mappings = {
#             "1": "algebra", "algebra": "algebra",
#             "2": "hangman", "hangman": "hangman",
#             "3": "quiz", "question": "quiz", "quiz": "quiz"
#         }
        
#         # Extract potential game choice
#         game_choice = next((word for word in user_message.split() 
#                           if word in game_mappings), None)
        
#         if game_choice:
#             game_type = game_mappings.get(game_choice)
#             if game_type:
#                 return jsonify({"response": f"Starting {game_type.title()} Game...", "game": game_type})
        
#         # If no valid game choice found, show options
#         return jsonify({
#             "response": "Which game would you like to play?\n1. Algebra - Practice math problems\n2. Hangman - Guess the word\n3. Quiz - Test your knowledge\n(You can enter either the number or name)"
#         })
    
#     elif "story" in user_message:
#         story = generate(story_model, start_str=user_message, predict_len=500)
#         return jsonify({"response": f"Here's your story:\n\n{story}"})
    
#     elif "music" in user_message or "song" in user_message:
#         emotion = predict_emotion(user_message, tokenizer, emotion_model, max_length, label_encoder)
#         song_link = show_song(emotion)
#         return jsonify({"response": f"I sense you're in the mood for {emotion}. Here's a song for you: {song_link}"})
    
#     else:
#         response = chatbot_response(user_message)
#         return jsonify({"response": response})

# @app.route('/game/<game_type>', methods=['POST'])
# def play_game(game_type):
#     data = request.json
    
#     if game_type == 'algebra':
#         user_answer = data.get('answer')
#         problem = data.get('problem', {})
#         correct_answer = problem.get('answer')
        
#         if user_answer == correct_answer:
#             return jsonify({"correct": True, "message": "Correct!"})
#         else:
#             return jsonify({"correct": False, "message": f"Incorrect. The answer was {correct_answer}"})
    
#     elif game_type == 'hangman':
#         guess = data.get('guess')
#         word = data.get('word')
#         guessed_letters = data.get('guessed_letters', [])
        
#         if guess in word and guess not in guessed_letters:
#             return jsonify({"correct": True, "message": "Good guess!"})
#         else:
#             return jsonify({"correct": False, "message": "Try again!"})
    
#     elif game_type == 'quiz':
#         answer = data.get('answer')
#         correct_answer = data.get('correct_answer')
        
#         if answer.lower() == correct_answer.lower():
#             return jsonify({"correct": True, "message": "Correct answer!"})
#         else:
#             return jsonify({"correct": False, "message": f"Wrong answer. The correct answer was: {correct_answer}"})

# if __name__ == "__main__":
#     app.run(debug=True)