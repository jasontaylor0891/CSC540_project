from flask import Flask, render_template, flash, redirect, url_for, request, session, logging
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from flask_wtf import Form
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, RadioField, SelectField, IntegerField
#from wtforms.fields.html5 import DateField
#from flask_script import Manager
from functools import wraps
from datetime import datetime


app = Flask(__name__, template_folder='templates')
app.secret_key = "welcome123"

#Change mysql host if not using docker. Docker default is gym_managment_db_1
app.config['MYSQL_HOST'] = 'gym_managment_db_1'
app.config['MYSQL_USER'] = 'gym'
app.config['MYSQL_PASSWORD'] = 'welcome123'
app.config['MYSQL_DB'] = 'gym'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

#function to determine if logged in to application.
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Nice try, Tricks don\'t work, bud!! Please Login :)', 'danger')
			return redirect(url_for('login'))
	return wrap

#function to determin if the logged in user is a trainer.
def is_trainer(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['profile'] == 3:
			return f(*args, **kwargs)
		else:
			flash('You are not a trainer!!, No access to this page.', 'danger')
			return redirect(url_for('login'))
	return wrap

#function to determin if the logged in user is a administrator.
def is_admin(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['profile'] == 1:
			return f(*args, **kwargs)
		else:
			flash('You are not an admin!!, No access to this page.', 'danger')
			return redirect(url_for('login'))
	return wrap

#function to determin if the logged in user is a receptionist.
def is_recep_level(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['profile'] <= 2:
			return f(*args, **kwargs)
		else:
			flash('You are not an authorised to view that page!!', 'danger')
			return redirect(url_for('login'))
	return wrap



#default route to the applications homepage
@app.route('/')
def index():
    return render_template("home.html"); 

#Login route.  This function logs the user into the application and determins their account profile
#and redirect the user to their appropriate dashboard.
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute('SELECT * FROM logins WHERE username = %s', [username])
        if result>0:
            data = cur.fetchone()
            cur.close()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['profile'] = data['profile']
                flash('You are logged in', 'success')
                if session['profile'] == 1:
                    return redirect(url_for('adminDashboard'))
                if session['profile'] == 3:
                    return redirect(url_for('trainerDashboard'))
                if session['profile'] == 2:
                    return redirect(url_for('receptionistDashboard'))
            
                return redirect(url_for('memberDashboard', username = username))
            else:
                error = 'Invalid login'
                return render_template('login.html', error = error)

		
        else:
            error = 'Username NOT FOUND'
            return render_template('login.html', error = error)

    return render_template('login.html')

    
@app.route('/adminDashboard')
@is_logged_in
@is_admin
def adminDashboard():
    return render_template("adminDashboard.html"); 

@app.route('/trainerDashboard')
@is_logged_in
@is_trainer
def trainerDashboard():
    return render_template("trainerDashboard.html"); 

@app.route('/receptionistDashboard')
@is_logged_in
@is_recep_level
def receptionistDashboard():
    return render_template("receptionistDashboard.html"); 

@app.route('/memberDashboard/<string:username>')
@is_logged_in
def memberDashboard(username):
    return render_template('memberDashboard.html')

@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))

@app.route('/registration', methods = ['GET', 'POST'])
@is_logged_in
def registration():
    return render_template('registration.html')

#if __name__ == "__main__":
app.run(host="0.0.0.0", port=int("5000"), debug=True)
