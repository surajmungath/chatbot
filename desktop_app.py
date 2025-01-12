import webview
import threading
from app1 import app

def start_server():
    app.run(host='127.0.0.1', port=5000)

def create_application():
    # Start Flask server in a separate thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    # Create a desktop window
    webview.create_window('Chatbot Application', 
                         'http://127.0.0.1:5000',
                         width=1000, 
                         height=800,
                         resizable=True)
    webview.start()

if __name__ == '__main__':
    create_application()
