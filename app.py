from flask import Flask, request, jsonify, render_template
from interf import chatbot_response
from game import algebra_practice_game, hangman_game, question_game
from inference import generate, model as story_model
from sentimentinf import predict_emotion, show_song, tokenizer, model as emotion_model, max_length, label_encoder

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip()
    
    if not user_input:
        return jsonify({'response': "I'm sorry, I didn't catch that. Can you try again?"})

    # Determine the intent and respond accordingly
    if "game" in user_input.lower():
        return jsonify({'response': handle_game_intent(user_input)})
    elif "story" in user_input.lower():
        return jsonify({'response': handle_story_intent(user_input)})
    elif "music" in user_input.lower() or "song" in user_input.lower():
        return jsonify({'response': handle_music_intent(user_input)})
    else:
        return jsonify({'response': chatbot_response(user_input)})

def handle_game_intent(user_input):
    if "algebra" in user_input:
        return "Algebra game feature is under development for the web."
    elif "hangman" in user_input:
        return "Hangman game feature is under development for the web."
    elif "quiz" in user_input:
        return "Quiz game feature is under development for the web."
    else:
        return "Please choose a valid game: algebra, hangman, or quiz."

def handle_story_intent(user_input):
    story_prompt = user_input.replace("story", "").strip() or "Once upon a time"
    story = generate(story_model, start_str=story_prompt, predict_len=500)
    return f"Here's your story:\n\n{story}"

def handle_music_intent(user_input):
    emotion = predict_emotion(user_input, tokenizer, emotion_model, max_length, label_encoder)
    song_link = show_song(emotion)
    return f"I sense you're in the mood for {emotion}. Here's a song for you: {song_link}"

if __name__ == '__main__':
    app.run(debug=True)
