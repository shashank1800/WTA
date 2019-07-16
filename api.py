from flask import Flask, render_template,request,redirect,url_for,session
from models.model import user_exists,save_user,product_exists,add_product,products_list,remove_from_db

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
		rs=user_exists(username)
		if rs:
			if rs['password']==password:
				session['username'] = username
				session['c_type']=rs['c_type']
				return render_template('home.html',title = 'Home',signin ="True")
		
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

@app.route('/products',methods=['GET','POST'])
def products():
	if request.method=='POST':
		product_info={}
		product_info['name']=request.form['name']
		product_info['price']=request.form['price']
		product_info['description']=request.form['description']
		product_info['seller']=session['username']
		if product_exists(product_info['name']):
			return "product exists"
		add_product(product_info)
		return redirect(url_for('home'))
	return render_template('products.html',products=products_list())

@app.route('/remove',methods=['GET','POST'])
def remove():
	if request.method=='POST':
		name=request.form['name']
		remove_from_db(name)
		return redirect(url_for('products'))
	return redirect(url_for('products'))
app.run(debug=True)
