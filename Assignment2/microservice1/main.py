from flask import Flask, render_template, request, redirect, url_for, session
from firestore_op import add_session, register_user, user_validation, update_session
import os

app = Flask(__name__)  # Create a Flask application instance

@app.route('/')  # Route for the home page
def index():
    return "hello world"

"""
Description: Code for register user 
Author: GeeksForGeek
Date: July 01, 2023
URL: https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
"""

@app.route('/register', methods=['GET', 'POST'])  # Route for the registration page
def register():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Retrieve the username, password, email, and location from the registration form
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        location = request.form['location']
        print(username, password, email, location)

        if register_user(username, password, email, location):
            # If registration is successful, add a session for the user with the state "created"
            if add_session(email, "created"):
                msg = 'You have successfully registered!'
            else:
                msg = 'Please fill out the form again!'
        else:
            msg = 'Please fill out the form again!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    # Render the registration template with the appropriate message
    return render_template('registration.html', msg=msg)

# Run the Flask application on the specified host and port
app.run(port=int(os.environ.get("PORT", 5001)), host='0.0.0.0', debug=True)
