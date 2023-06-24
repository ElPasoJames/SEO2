import os
import requests
from flask import Flask, flash, redirect, render_template, session, request, url_for
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import core


current_folder = os.path.dirname(os.path.abspath(__file__))
#file_name = "fbAdminConfig.json"
#cred = credentials.Certificate(file_name)

app = Flask(__name__)
app.secret_key = 'gpt-secret-key'

API_KEY = 'IzaSyCLEPrZxeYkN73c5vAb-BBqdn2dVAxyJ0Q'
AUTH_API_BASE_URL = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input1 = request.form['input1']
        input2 = request.form['input2']
        input3 = request.form['input3']
        inputs = [input1, input2, input3]
        result = core.process_gpt(inputs)

        flash(result)

    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate the user's email and password with Firebase
        response = requests.post(f'{AUTH_API_BASE_URL}', json={
            'email': email,
            'password': password,
            'returnSecureToken': True
        })

        if response.ok:
            # Store the Firebase ID token in a session variable or cookie
            session['user'] = response.json()['localId']
            session['logged_in'] = True

            # Redirect to a protected page that requires authentication
            return redirect('/')
        else:
            # Handle any errors that occur during authentication
            # error_message = response.json().get('error', {}).get('message', 'Invalid email or password.')
            error_message = 'Invalid email or password.'
            flash(error_message)
    return render_template('login.html')



# Use a service account.
cred = credentials.Certificate("fbAdminConfig.json")

application = firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # create user Firebase Authentification
        user = firebase_admin.auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            disabled=False)

        # if firebase authentication false return error
        if user is None:
            return render_template('register.html', error='Failed to create user')

        #If firebase authentication successfull then save user in Firestore database retrieve user uid from Firebase Authentification
        uid = user.uid
        # user = firebase_admin.auth.get_user(user.uid)

        #Save user in Firestore database after user created in Firebase Authentification
        #doc_ref = firestore.collection('Users').document(user.uid)
        doc_ref = db.collection('Users').document(uid)
        doc_ref.set({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        })


        return redirect('/')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/logout')
def logout():
    # Clear the session data and log the user out of Firebase
    session.pop('logged_in', None)
    # auth.revoke_refresh_tokens(session['user'])
    return redirect('/')    

if __name__ == '__main__':
    app.run(debug=True)


