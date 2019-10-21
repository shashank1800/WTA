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
database = firebase.database()

db = firebase.database()

source_destination = ""
all_bus_list = []

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

@app.route("/show_bus_list",methods=['GET', 'POST'])
def show_bus_list():
	if (request.method == 'POST'):
		source = request.form['source'].lower()
		destination = request.form['destination'].lower()

	source_destination = source+"-"+destination

	date_wise = dict()
	root_wise = dict()
	all_bus_list = []

	data1 = db.child("date-wise").child("22-10-2019").child(source_destination).get()
	for user in data1.each():
		date_wise[user.key()] = user.val()
	data2 = db.child("bus_list").child(source_destination).get()
	for user in data2.each():
		root_wise[user.key()] = user.val()


	for bus in date_wise:
		full_bus_detail = dict()
		for opt in date_wise[bus]:
			full_bus_detail[opt] = date_wise[bus][opt]
		for opt in root_wise[bus]:
			full_bus_detail[opt] = root_wise[bus][opt]
		all_bus_list.append(full_bus_detail)

	return render_template('show_bus_list.html',all_bus_list=all_bus_list)

@app.route("/developers")
def developers():
	return render_template('developers.html')

@app.route("/show_seats", methods = ['GET','POST'])
def show_seats():
	return render_template('home.html')


app.run(debug=False)
app.do_teardown_appcontext()