from flask import Flask, render_template,request,redirect,url_for,session

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
		users = {'user1':'123','a':'a'}
		username= request.form['username']
		password= request.form['password']
	
		if username not in users:
			return "! User"

		if users[username] != password:
			return "! Password"

		session['username'] = username

		return redirect(url_for('home'))

	return render_template('login.html',title = 'About')

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('home'))

app.run(debug=True)
