import torch
import torch.nn as nn
import numpy as np
import pickle
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Define the CharRNN model
class CharRNN(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers):
        super(CharRNN, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden):
        x = self.embedding(x)
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out.reshape(out.size(0) * out.size(1), out.size(2)))
        return out, hidden

    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        hidden = (weight.new(self.num_layers, batch_size, self.hidden_size).zero_(),
                  weight.new(self.num_layers, batch_size, self.hidden_size).zero_())
        return hidden

# Load the vocabulary and mappings
with open("char_to_idx.pkl1", "rb") as f:
    char_to_idx = pickle.load(f)
idx_to_char = {i: ch for ch, i in char_to_idx.items()}
vocab_size = len(char_to_idx)

# Model configuration
hidden_size = 256  # Must match the trained model
num_layers = 2     # Must match the trained model

# Load the trained model
def load_model():
    model = CharRNN(vocab_size, hidden_size, num_layers)
    # Use weights_only=True to avoid the pickle security warning
    model.load_state_dict(torch.load("storygen.pth", map_location=torch.device('cpu'), weights_only=True))
    model.eval()
    return model

try:
    model = load_model()
except Exception as e:
    print(f"Error loading story generation model: {str(e)}")
    model = None

# Function to generate text
def generate(model, start_str, predict_len=300, temperature=0.7):
    if model is None:
        return None
    
    try:
        model.eval()
        hidden = model.init_hidden(1)
        
        # Add a story starter if the input is very short
        if len(start_str) < 5:
            start_str = f"Once upon a time, there was a {start_str} who "
            
        # Filter out characters not in vocabulary
        start_str = ''.join(ch for ch in start_str if ch in char_to_idx)
        if not start_str:
            start_str = "Once upon a time"  # Default if no valid characters
            
        start_input = torch.tensor([char_to_idx[ch] for ch in start_str], dtype=torch.long).unsqueeze(0)
        predicted = start_str

        with torch.no_grad():
            for p in range(len(start_str) - 1):
                _, hidden = model(start_input[:, p].unsqueeze(0), hidden)
            inp = start_input[:, -1]

            for _ in range(predict_len):
                output, hidden = model(inp.unsqueeze(0), hidden)
                output_dist = output.data.view(-1).div(temperature).exp()
                top_i = torch.multinomial(output_dist, 1)[0]
                predicted_char = idx_to_char[top_i.item()]
                predicted += predicted_char
                inp = torch.tensor([top_i], dtype=torch.long)

        return predicted

    except Exception as e:
        print(f"Error in story generation: {str(e)}")
        return None

if __name__ == "__main__":
    start_string = "Once upon a time"
    generated_story = generate(model, start_string)
    print(generated_story)
