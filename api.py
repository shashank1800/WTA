from flask import Flask, render_template,request,redirect,url_for,session

from models.model import user_exists,save_user

app = Flask(__name__)
app.secret_key = 'hello'

@app.route("/")
def home():
	return render_template('home.html',title='Home')

@app.route("/contact")
def contact():
	return render_template('contact.html',title='Contact')

@app.route("/about")
def about():
	return render_template('about.html',title = 'About')

@app.route("/login",methods=['GET','POST'])
def login():
	if request.method == 'POST':
		
		username= request.form['username']
		password= request.form['password']
		result = user_exists(username)

		if result['password'] == password:
			session['username'] = username
			session['c_type'] = result['c_type']
			return render_template('home.html',title = 'Home',signin = "true")

	return render_template('login.html',title = 'Login')

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('home'))

@app.route("/signup",methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		user_info={}
		user_info['username'] =  request.form['username']
		user_info['password'] = request.form['password1']
		username = request.form['username']
		password1 = request.form['password1']
		password2 = request.form['password2']
		user_info['c_type'] =request.form['type']
		if user_info['c_type'] == 'buyer':
			user_info['cart'] = []

		if user_exists(user_info['username']):
			return "username already exists"

		if user_info['password'] != password2:
			return "Password didn't match"

		save_user(user_info)

	return(redirect(url_for('home')))

app.run(debug=True)
