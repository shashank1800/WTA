from pymongo import MongoClient
from flask import redirect,url_for,session

client=MongoClient("mongodb://localhost:27017")
db=client['amazon']

def user_exists(username):
	query={'username':username}
	result=db['users'].find_one(query)
	if bool(result):
		return result
	return False

def save_user(user_info):
	db['users'].insert_one(user_info)

def product_exists(productname):
	query={'name':productname}
	result=db['products'].find_one(query)
	if bool(result):
		return result
	return False

def add_product(product_info):
	db['products'].insert_one(product_info)

def products_list():
	if session['c_type']=='seller':
		result=db['products'].find({})
		return result
	query={"seller":session['username']}
	result=db['products'].find(query)
	return result

def remove_from_db(name):
	query={"name":name}
	db['products'].remove(query)
	return redirect(url_for('products'))