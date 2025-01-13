import sys
import os

# Add the directory containing your app to the Python path
path = '/home/yourusername/chatbot'  # Replace with your PythonAnywhere username
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app1 import app as application

# Optional: Configure logging
import logging
logging.basicConfig(filename='/home/yourusername/chatbot/flask_error.log', level=logging.DEBUG)
