from flask import Flask, render_template
from firestore_op import get_online_session
# Import necessary modules and functions

app = Flask(__name__)  # Create a Flask application instance
import os

@app.route('/')  # Route for the home page
def index():
    return "hello world"

# The following route is for displaying the list of logged-in users
# The code is taken from: https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/
@app.route('/who_is_online', methods=['GET', 'POST'])
def get_login_list():
    msg = ''

    # Retrieve the list of online users using the get_online_session() function
    login_user = get_online_session()

    # Render the template 'login_people.html' and pass the 'login_user' list as a variable called 'people'
    return render_template('login_people.html', people=login_user)

# Run the Flask application on the specified host and port
app.run(port=int(os.environ.get("PORT", 5003)), host='0.0.0.0', debug=True)
