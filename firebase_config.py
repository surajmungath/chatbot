import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Initialize Firebase Admin
if 'FIREBASE_CONFIG' in os.environ:
    # For production (Render)
    cred_dict = json.loads(os.environ.get('FIREBASE_CONFIG'))
    cred = credentials.Certificate(cred_dict)
else:
    # For local development
    current_dir = os.path.dirname(os.path.abspath(__file__))
    service_account_path = os.path.join(current_dir, 'serviceAccountKey.json')
    cred = credentials.Certificate(service_account_path)

firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()
