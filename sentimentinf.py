from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
import os
import tensorflow as tf

# Step 1: Load Model, Tokenizer, and Label Encoder
try:
    # Configure TensorFlow to use CPU
    tf.config.set_visible_devices([], 'GPU')
    
    # Set up model loading with custom objects if needed
    model = load_model('emotion_model.h5', compile=False)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    tokenizer = joblib.load('tokenizer.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    
    # Define max_length based on training
    max_length = 66  # Hardcoding this since we know the value
except Exception as e:
    print(f"Error loading emotion model: {str(e)}")
    model = None
    tokenizer = None
    label_encoder = None
    max_length = 66

# Step 2: Define Inference Function
def predict_emotion(text, tokenizer, model, max_length, label_encoder):
    """
    Predict the emotion of a given text input.

    Args:
        text (str): Input text to classify.
        tokenizer (Tokenizer): Fitted tokenizer for preprocessing.
        model (Sequential): Trained Keras model for prediction.
        max_length (int): Maximum length used during model training.
        label_encoder (LabelEncoder): Encoder for decoding emotion labels.

    Returns:
        str: Predicted emotion label.
    """
    if any(x is None for x in [model, tokenizer, max_length, label_encoder]):
        return "neutral"  # Default emotion if model not loaded
        
    try:
        # Tokenize and pad the input text
        sequence = tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(sequence, maxlen=max_length)
        # Predict emotion
        prediction = model.predict(padded_sequence)
        emotion_index = prediction.argmax()  # Get the index of the highest probability
        emotion_label = label_encoder.inverse_transform([emotion_index])[0]  # Decode to emotion label
        return emotion_label
    except Exception as e:
        print(f"Error predicting emotion: {str(e)}")
        return "neutral"  # Default emotion on error

# Step 3: Define Function to Show YouTube Link
def show_song(emotion):
    """
    Return a YouTube link based on the emotion.

    Args:
        emotion (str): Predicted emotion label.

    Returns:
        str: YouTube link or message for the emotion.
    """
    emotion_songs = {
        "fear": "https://www.youtube.com/watch?v=6Ejga4kJUts",  # The Sound of Silence
        "joy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",   # Happy - Pharrell Williams
        "sadness": "https://www.youtube.com/watch?v=4N3N1MlvVc4", # Mad World
        "anger": "https://www.youtube.com/watch?v=5abamRO41fE",   # Breaking the Habit
        "surprise": "https://www.youtube.com/watch?v=L_jWHffIx5E", # All Star
        "neutral": "https://www.youtube.com/watch?v=rYEDA3JcQqw",  # Rolling in the Deep
        "disgust": "https://www.youtube.com/watch?v=4V90AmXnguw",  # Stronger
        "love": "https://www.youtube.com/watch?v=450p7goxZqg",     # All of Me
    }
    return emotion_songs.get(emotion, "No song available for this emotion.")

# Step 4: Get Input from User
if __name__ == "__main__":
    while True:
        user_text = input("Enter a text to analyze emotion (or type 'exit' to quit): ")
        if user_text.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        predicted_emotion = predict_emotion(user_text, tokenizer, model, max_length, label_encoder)
        print(f"Predicted Emotion: {predicted_emotion}")
        show_song(predicted_emotion)
