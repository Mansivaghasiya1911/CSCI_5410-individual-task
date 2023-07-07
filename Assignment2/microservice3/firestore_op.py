import firebase_admin
from firebase_admin import firestore
import os
from datetime import datetime

"""
Description: Data connection with Firestore 
Date: July 01, 2023
URL: https://firebase.google.com/docs/firestore/quickstart
"""


# Set the path to the Google Cloud credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./cloud-computing-389018-ae1f308e672f.json"

# Initialize the Firebase app using application default credentials
app = firebase_admin.initialize_app()
db = firestore.client()

def register_user(name, password, email, location):
    try:
        user_data = {
            "email": email,
            "location": location,
            "password": password,
            "user_name": name
        }

        # Add user data to the "user-details" collection in Firestore
        db.collection("user-details").add(user_data)
    except Exception as e:
        print("An error occurred:", e)
        return False

    return True

def add_session(email, state):
    try:
        session_data = {
            "email": email,
            "state": state,
            "time_stamp": datetime.fromtimestamp(datetime.timestamp(datetime.now()))
        }

        # Add session data to the "state" collection in Firestore
        db.collection("state").add(session_data)
    except Exception as e:
        print("An error occurred:", e)
        return False

    return True

def user_validation(email, password):
    user_valid = False
    user_name = ""
    try:
        # Query the "user-details" collection to find the user with the specified email
        get_data = db.collection('user-details').where("email", "==", email)

        for doc in get_data.stream():
            obj = doc.to_dict()
            if obj["password"] == password:
                user_valid = True
                user_name = obj["user_name"]
            print("password:", obj["password"])
    except Exception as e:
        print("An error occurred:", e)

    return user_valid, user_name

def update_session(email, state):
    session_updated = False
    try:
        new_session_data = {
            "email": email,
            "state": state,
            "time_stamp": datetime.fromtimestamp(datetime.timestamp(datetime.now()))
        }

        # Query the "state" collection to find the session with the specified email
        get_data = db.collection('state').where("email", "==", email)
        document_id = ""
        for doc in get_data.stream():
            document_id = doc.id

        # Update the session data in Firestore
        doc_ref = db.collection("state").document(document_id)
        doc_ref.update(new_session_data)
        session_updated = True
    except Exception as e:
        print("An error occurred:", e)

    return session_updated

def get_online_session():
    login_user_info = []
    try:
        # Query the "state" collection to find all sessions with the state "login"
        get_data = db.collection('state').where("state", "==", "login")

        for doc in get_data.stream():
            obj = doc.to_dict()
            login_user_info.append(obj["email"])
    except Exception as e:
        print("An error occurred:", e)

    return login_user_info
