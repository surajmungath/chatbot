# Deployment on PythonAnywhere

## Prerequisites
1. Create a free or paid PythonAnywhere account
2. Open a Bash console in PythonAnywhere

## Setup Steps
1. Clone the repository:
```bash
git clone https://github.com/surajmungath/chatbot.git
cd chatbot
```

2. Create a virtual environment:
```bash
mkvirtualenv --python=/usr/bin/python3.11 chatbot_env
workon chatbot_env
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download NLTK data:
```bash
python -m nltk.downloader punkt
python -m nltk.downloader wordnet
```

5. Web App Configuration
- Go to the Web tab
- Add a new web app
- Choose manual configuration
- Python version: 3.11
- Virtualenv path: `/home/yourusername/.virtualenvs/chatbot_env`
- Source code: `/home/yourusername/chatbot`
- Working directory: `/home/yourusername/chatbot`
- WSGI configuration file: `/home/yourusername/chatbot/wsgi.py`

## Environment Variables
Set these in the PythonAnywhere Web app configuration:
- FLASK_ENV=production
- SECRET_KEY=your_secret_key
- FIREBASE_CONFIG=your_firebase_config_json

## Troubleshooting
- Check logs at: `/home/yourusername/chatbot/flask_app.log`
- Ensure all dependencies are installed
- Verify file permissions

## Notes
- Always activate the virtual environment before running or debugging
- Restart the web app after making significant changes
