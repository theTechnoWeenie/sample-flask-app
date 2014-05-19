import string, random, argparse, os
from flask import Flask, request, redirect, render_template, url_for, send_from_directory, jsonify
from flask.ext.wtf import Form
from wtforms import TextField, validators


app = Flask(__name__)

@app.route('/')
def index():
    """Homepage. If a name is supplied via query params, that name will be"""
    name = "world"
    name = request.args.get("name", name)
    return "Hello, %s!"%name

@app.route('/a-redirect')
def a_redirect():
	"""Redirect the user to /"""
	print "Move along, there's nothing to see here."
	return redirect(url_for("index"))

@app.route('/user/<int:id>')
def get_user(id):
	"""This function echos back the supplied URL param"""
	return "The user profile for %d"%id

@app.route('/user/<int:id>/json')
def get_items(id):
	"""This function echos a json blob for the id specified."""
	#return "The items for user %d"%id
	userItems = {'userId':id}
	return jsonify(**userItems)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
	"""Does zero auth, but will greet the user when they 'log' in"""
	if request.method == 'POST':
		return "Hello, %s"%(request.form['userName'])
	return render_template('login.html')

@app.route('/testForm', methods=['GET', 'POST'])
def formPage():
	"""This is a more complex example of a form that programmatically generated. 
	This validates email address with a basic validator, and shows the error if there is a problem."""
	form = RegistrationForm()
	name = "world"
	if form.validate_on_submit():
		name = form.name.data
		print "User %s with email %s just registered"%(name, form.email.data)
	return render_template('template.html', name=name, form=form) #parameters passed here will be available to the template.

@app.route('/favicon.ico')
def favicon():
	"""Provides the resource for the favicon. In our case stored in assests"""
	path = os.path.join(app.root_path, 'assets')
	return send_from_directory(path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

class RegistrationForm(Form):
	"""This is a sample of using a form from Flask-WTF"""
	name = TextField('Name')
	#create a text field with a validator.
	email = TextField('Email', [validators.Email()])


def get_args():
	"""A simple function to parse the command line parameters via argparse"""
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--debug", help="Turn on debug mode.", action="store_true")
	parser.add_argument("-i", "--ipaddress", help="specify the ip address to run the application on <default=0.0.0.0>")
	return parser.parse_args()

if __name__ == "__main__":
	args = get_args()
	#secret key must be used or secure forms must be turned off.
	app.secret_key = '@X\x01L \x9eN\xc8\xa9\x01\xd8\xe3\x0b\x1d\n\xce\x8e\xde\xef\x00\xab\x9c\xe2\xc7'
	host = "0.0.0.0" #this is 'any ip'
	if args.ipaddress is not None:
		host = args.ipaddress

	app.run(debug=args.debug, host=host)