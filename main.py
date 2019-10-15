import pyrebase
import os

from flask import Flask,render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key = 'random string'

config = {
    "apiKey": "AIzaSyDgMvPsK5gW9EZqs4dMRxLxbH5-kKIX0PA",
    "authDomain": "wta-255710.firebaseapp.com",
    "databaseURL": "https://wta-255710.firebaseio.com",
    "projectId": "wta-255710",
    "storageBucket": "wta-255710.appspot.com",
    "messagingSenderId": "94348458304",
    "appId": "1:94348458304:web:fa280ae1fed8aa00db22a5",
    "measurementId": "G-1RLXVSEK27"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route("/")
def home():
	if session.get('email',False):
		return render_template('home.html')
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	try:
		if (request.method == 'POST'):
			email = request.form['name']
			password = request.form['password']
			user = auth.sign_in_with_email_and_password(email, password)
			session['email'] = email
			return render_template('home.html')

	except:
		flash('Something went wrong!!')

	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

	if (request.method == 'POST'):
		email = request.form['name']
		password1 = request.form['password']
		password2 = request.form['confirm_password']

		if password1 == password2 and password1!="" and email!="":
			user = auth.create_user_with_email_and_password(email, password1)
			user = auth.refresh(user['refreshToken'])
			auth.send_email_verification(user['idToken'])
			user = auth.sign_in_with_email_and_password(email, password1)
			session['email'] = email
			return render_template('home.html')

	return render_template('register.html')

@app.route("/forgot_password")
def forgot_password():
	return render_template('forgot_password.html')

@app.route("/forgot_form",methods=['GET', 'POST'])
def forgot_form():
	if (request.method == 'POST'):
		email = request.form['name']

		if email!="":
			auth.send_password_reset_email(email)

	return render_template('login.html')

@app.route("/logout")
def logout():
	session.pop("email",None)
	return render_template('login.html')

@app.route("/show_bus_list")
def show_bus_list():
	return render_template('show_bus_list.html')

app.run(debug=True)
app.do_teardown_appcontext()