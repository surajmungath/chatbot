from flask import Flask, render_template, request, jsonify, url_for, redirect, session
import nltk_setup
from interf import chatbot_response
from game import AlgebraGame, HangmanGame, QuizGame
from inference import generate, model as story_model
from sentimentinf import predict_emotion, show_song, tokenizer, model as emotion_model, max_length, label_encoder
import tensorflow as tf
import io
from contextlib import redirect_stdout
import os
import random

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)  # for session management

# Game state storage
game_states = {}

def capture_output(func, *args, **kwargs):
    """Capture the output of functions that print to stdout"""
    f = io.StringIO()
    with redirect_stdout(f):
        result = func(*args, **kwargs)
    output = f.getvalue()
    return output, result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('chat_page'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('sing.html')

@app.route('/chat')
def chat_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/chat.html')
def chat_html_redirect():
    return redirect(url_for('chat_page'))

@app.route('/process_chat', methods=['POST'])
def process_chat():
    if 'user' not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
            
        user_id = session['user']
        
        # Check if we're waiting for story topic
        if session.get('awaiting_story_topic') and user_message.lower() != "story":
            session.pop('awaiting_story_topic', None)  # Clear the flag
            return handle_story_request(user_message)
            
        # Check if we're waiting for story type
        if session.get('awaiting_story_type'):
            session.pop('awaiting_story_type', None)  # Clear the flag
            return handle_story_request(user_message)
            
        # Check if we're waiting for mood
        if session.get('awaiting_mood'):
            session.pop('awaiting_mood', None)  # Clear the flag
            try:
                return handle_music_request(user_message)
            except Exception as e:
                app.logger.error(f"Error in music request: {str(e)}")
                return jsonify({"error": "Unable to process music request. Please try again."}), 500
        
        # Game intent
        if any(word in user_message.lower() for word in ["play", "game", "algebra", "hangman", "quiz"]):
            return handle_game_request(user_message, user_id)
        
        # Check for story keyword in any input
        elif "story" in user_message.lower():
            session['awaiting_story_type'] = True
            return jsonify({"response": "what would you like the story to be about?\n Please tell me a topic:"})
            
        # Check for music keyword in any input
        elif "music" in user_message.lower() or "song" in user_message.lower():
            session['awaiting_mood'] = True
            return jsonify({"response": "How are you feeling right now? Tell me your mood:"})
        
        # Default chatbot response
        else:
            response = chatbot_response(user_message)
            if not response:
                return jsonify({"error": "Unable to generate response"}), 500
                
            # Handle both string and dictionary responses for backward compatibility
            if isinstance(response, str):
                return jsonify({"response": response})
            else:
                return jsonify({"response": response.get("text", ""), "suggestions": response.get("suggestions", [])})
            
    except ValueError as e:
        app.logger.error(f"Value error in chat endpoint: {str(e)}")
        return jsonify({"error": "Invalid input format"}), 400
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

@app.route('/game/answer', methods=['POST'])
def handle_game_answer():
    if 'user' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session['user']
    if user_id not in game_states:
        return jsonify({"error": "No active game"}), 400
    
    data = request.get_json()
    game_type = data.get('game_type')
    answer = data.get('answer')
    
    if not game_type or not answer:
        return jsonify({"error": "Missing game_type or answer"}), 400
    
    if game_type == 'algebra':
        return handle_algebra_answer(user_id, answer)
    elif game_type == 'hangman':
        return handle_hangman_guess(user_id, answer)
    elif game_type == 'quiz':
        return handle_quiz_answer(user_id, answer)
    else:
        return jsonify({"error": "Invalid game type"}), 400

def handle_game_request(user_message, user_id):
    # Initialize game states for user if not exists
    if user_id not in game_states:
        game_states[user_id] = {}

    # Check for game selection
    game_type = None
    if "algebra" in user_message.lower():
        game_type = "algebra"
    elif "hangman" in user_message.lower():
        game_type = "hangman"
    elif "quiz" in user_message.lower():
        game_type = "quiz"

    if game_type:
        # Initialize the selected game
        if game_type == "algebra":
            game = AlgebraGame()
            problem = game.generate_problem()
            game_states[user_id]['algebra'] = {
                'problem': problem,
                'score': 0,
                'problems_solved': 0
            }
            return jsonify({
                "response": "Let's play Algebra! Solve this problem:",
                "game_type": "algebra",
                "game_data": {"problem": problem["problem"]}
            })
        elif game_type == "hangman":
            game = HangmanGame()
            game_state = game.new_game()
            game_states[user_id]['hangman'] = game_state
            return jsonify({
                "response": "Let's play Hangman! Guess the word:",
                "game_type": "hangman",
                "game_data": {
                    "category": game_state['category'],
                    "display": game_state['display'],
                    "guessed": game_state['guessed'],
                    "chances": game_state['chances']
                }
            })
        elif game_type == "quiz":
            game = QuizGame()
            question = game.get_random_question()
            game_states[user_id]['quiz'] = {
                'current_question': question,
                'score': 0,
                'questions_answered': 0
            }
            return jsonify({
                "response": "Let's play Quiz! Answer this question:",
                "game_type": "quiz",
                "game_data": {"question": question["question"]}
            })
    
    return jsonify({
        "response": "Which game would you like to play? Type:\n- 'algebra' for math practice\n- 'hangman' to guess words\n- 'quiz' to test your knowledge"
    })

def handle_algebra_answer(user_id, answer):
    game_state = game_states[user_id].get('algebra')
    if not game_state:
        return jsonify({"error": "No active algebra game"}), 400
    
    try:
        answer = float(answer)
        current_problem = game_state['problem']
        is_correct = abs(answer - current_problem['answer']) < 0.01
        
        if is_correct:
            game_state['score'] += 1
            message = "Correct!"
        else:
            message = f"Incorrect.\nQuestion: {current_problem['problem']}\nYour answer: {answer}\nCorrect answer: {current_problem['answer']}"
        
        game_state['problems_solved'] += 1
        
        if game_state['problems_solved'] < 5:
            game = AlgebraGame()
            new_problem = game.generate_problem()
            game_state['problem'] = new_problem
            return jsonify({
                "message": message,
                "game_data": {"problem": new_problem["problem"]}
            })
        else:
            final_score = game_state['score']
            del game_states[user_id]['algebra']
            return jsonify({
                "message": f"{message}\nGame Over! Your final score is {final_score}/5",
                "game_over": True
            })
    except ValueError:
        return jsonify({"error": "Invalid answer format"}), 400

def handle_hangman_guess(user_id, guess):
    game_state = game_states[user_id].get('hangman')
    if not game_state:
        return jsonify({"error": "No active hangman game"}), 400
    
    try:
        result = HangmanGame.make_guess(game_state, guess)
        
        # Format display properly
        if isinstance(game_state['display'], list):
            result['display'] = " ".join(game_state['display'])
        
        # Format guessed letters properly
        if isinstance(game_state['guessed'], list):
            result['guessed'] = ", ".join(game_state['guessed'])
        
        if game_state['status'] != 'playing':
            del game_states[user_id]['hangman']
            result['game_over'] = True
        
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error in hangman guess: {str(e)}")
        return jsonify({"error": "Error processing your answer. Please try again."}), 500

def handle_quiz_answer(user_id, answer):
    game_state = game_states[user_id].get('quiz')
    if not game_state:
        return jsonify({"error": "No active quiz game"}), 400
    
    current_question = game_state['current_question']
    is_correct = QuizGame.check_answer(answer, current_question['answer'])
    
    if is_correct:
        game_state['score'] += 1
        message = "Correct!"
    else:
        message = f"Incorrect.\nQuestion: {current_question['question']}\nYour answer: {answer}\nCorrect answer: {current_question['answer']}"
    
    game_state['questions_answered'] += 1
    
    if game_state['questions_answered'] < 5:
        quiz = QuizGame()
        new_question = quiz.get_random_question()
        game_state['current_question'] = new_question
        return jsonify({
            "message": message,
            "game_data": {"question": new_question["question"]}
        })
    else:
        final_score = game_state['score']
        del game_states[user_id]['quiz']
        return jsonify({
            "message": f"{message}\nGame Over! Your final score is {final_score}/5",
            "game_over": True
        })

def handle_story_request(story_type):
    try:
        prompt = f"{story_type}"
        story = generate(story_model, prompt)
        return jsonify({"response": story})
    except Exception as e:
        app.logger.error(f"Error generating story: {str(e)}")
        return jsonify({"response": "I'm having trouble generating a story right now. Please try again later."})

def get_music_recommendation():
    recommendations = [
        "I recommend listening to 'Bohemian Rhapsody' by Queen - a classic rock masterpiece!",
        "Check out 'Shape of You' by Ed Sheeran - a catchy pop hit!",
        "Try 'Hotel California' by Eagles - an iconic rock song!",
        "You might enjoy 'Billie Jean' by Michael Jackson - the king of pop!",
        "How about 'Sweet Child O' Mine' by Guns N' Roses - a rock anthem!",
        "Listen to 'Rolling in the Deep' by Adele - a powerful ballad!",
        "Check out 'Uptown Funk' by Mark Ronson ft. Bruno Mars - a funky hit!",
        "Try 'Stairway to Heaven' by Led Zeppelin - a rock legend!",
        "I recommend 'Someone Like You' by Adele - a beautiful love song!",
        "You might like 'Smells Like Teen Spirit' by Nirvana - grunge classic!"
    ]
    return f" Music Recommendation: {random.choice(recommendations)}"

def handle_music_request(mood):
    try:
        # Predict emotion from user's mood
        emotion = predict_emotion(mood, tokenizer, emotion_model, max_length, label_encoder)
        
        # Get song URL based on emotion
        url = show_song(emotion)
        
        # Get a random recommendation
        recommendation = get_music_recommendation()
        
        # Format the response with both recommendation and URL in button format
        return jsonify({
            "response": f"Based on your mood {emotion},\n\n here's a song for you: <url>{url}</url>"
        })
    except Exception as e:
        app.logger.error(f"Error processing music request: {str(e)}")
        return jsonify({"response": "I'm having trouble processing your music request. Please try again later."})

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.json
        user_id = session['user']
        
        # Update user profile in Firestore
        user_ref = db.collection('users').document(user_id)
        user_ref.set({
            'name': data.get('name'),
            'email': data.get('email'),
            'updated_at': firestore.SERVER_TIMESTAMP
        }, merge=True)
        
        return jsonify({"success": True, "message": "Profile updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/auth', methods=['POST'])
def auth():
    try:
        auth_data = request.json
        session['user'] = auth_data.get('email')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
