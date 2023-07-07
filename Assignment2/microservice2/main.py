from flask import Flask, render_template, request, redirect, url_for, session
from firestore_op import add_session, register_user, user_validation, update_session
from flask_session import Session
import os

app = Flask(__name__)  # Create a Flask application instance

# Configure the Flask application to use filesystem-based sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')  # Route for the home page
def index():
    return "hello world"

"""
Description: Code for register user 
Author: GeeksForGeek
Date: July 01, 2023
URL: https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        msg = "Kindly provide your details"
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        valid_user, user_name = user_validation(email, password)

        if valid_user:
            print("User validated")
            if update_session(email, "login"):
                print("Session added")
                session["email"] = email
                session["user_name"] = user_name
                return redirect("/home")
        else:
            msg = "Your email or password is not correct"

    # Render the login template with the appropriate message
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    email = session.get("email")
    if update_session(email, "logout"):
        print("Session removed")
        return redirect("/register")
    return "You are logged out"

@app.route('/home')
def home():
    # Render the home template and pass the user's name from the session as a variable
    return render_template('home.html', name=session.get("user_name"))

# Run the Flask application on the specified host and port
app.run(port=int(os.environ.get("PORT", 5002)), host='0.0.0.0', debug=True)
