from flask import Flask, render_template, flash, redirect, url_for, request, session, logging
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, TextAreaField, PasswordField, validators, RadioField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#from flask_wtf import Form
#from wtforms import Form, StringField, TextAreaField, PasswordField, validators, RadioField, SelectField, IntegerField
#from wtforms.validators import Required
#from wtforms.fields.html5 import DateField
#from flask_script import Manager

from functools import wraps
from datetime import datetime
#from forms import AddMemberForm

app = Flask(__name__, template_folder='templates')
app.secret_key = "welcome123"

#Change mysql host if not using docker. Docker default is gym_managment_db_1
app.config['MYSQL_HOST'] = 'csc540_project-db-1'
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

userAge = []
userGender = []
menberType = []
values = []

class AddMemberForm(Form):

	#Class to define the Add Member Form
    address = StringField('Address', [validators.Length(min=1, max=75), validators.InputRequired()])
    city = StringField('City', [validators.Length(min=1, max=25), validators.InputRequired()])
    zipCode = StringField('Zip Code', [validators.Length(min=1, max=75), validators.InputRequired()])
    fname = StringField('First Name', [validators.Length(min=1, max=50), validators.InputRequired()])
    lname = StringField('Last Name', [validators.Length(min=1, max=50), validators.InputRequired()])
    username = StringField('Username', [validators.InputRequired(), validators.NoneOf(values = values, message = "Username is already taken")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    age = SelectField('Age', choices = userAge)
    gender = SelectField('Gender', choices = userGender)
    mtype = SelectField('Membership Type', choices = menberType)

@app.route('/registration', methods = ['GET', 'POST'])
#@is_logged_in
def registration():

	#Clear the lists
	menberType.clear()
	userGender.clear()
	userAge.clear()
	values.clear()

	#Create the list for the age SelectField
	x = range(16, 100)
	for i in x:
	    userAge.append(i)

	#Create the list for the gender list
	userGender.append("Male")
	userGender.append("Female")
	userGender.append("Other")
	
	#Create the list for the membership types
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT membershipsTypesName from membershipsTypes")
	b = cur.fetchall()
	for i in range(q):
	    menberType.append(b[i]['membershipsTypesName'])

	#Create the list of usersnames
	q = cur.execute("SELECT username FROM logins")
	b = cur.fetchall()
	for i in range(q):
	    values.append(b[i]['username'])

	form = AddMemberForm(request.form)
	if request.method == 'POST':

		#Get the data from the form
		username = request.form['username']
		fname = request.form['fname']
		lname = request.form['lname']
		password = request.form['password']
		age = request.form['age']
		gender = request.form['gender']
		mtype = request.form['mtype']
		address = request.form['address']
		city = request.form['city']
		zipCode = request.form['zipCode']

		#Get membership_id from user slection
		if mtype == 'Platinum':
			mtypeId = 1
		if mtype == 'Gold':
			mtypeId = 2
		if mtype == 'Sliver':
			mtypeId = 3

		#Get membership fee from user slection
		result = cur.execute('SELECT fee from membershipsTypes WHERE membershipsTypesName = %s', [mtype])
		data = cur.fetchone()
		mfee = data['fee']	
		
		#Update logins table
		hash = sha256_crypt.hash(password)
		sql = "INSERT INTO logins(username, password, profile) VALUES('" +username+ "', '" +hash+ "', 4)"
		cur.execute(sql)
		mysql.connection.commit()

		#Update Customers Table
		sql = "INSERT INTO Customers(firstName, lastName, age, gender, Address, city, zipCode, membership_ID, membership_type, fee, username, branch_No) VALUES( '" +fname+ "', '" +lname+ "', " +str(age)+", '" +gender+"', '"+address+"', '"+city+"', '" +zipCode+"', " +str(mtypeId)+", '"+mtype+"', "+str(mfee)+", '"+username+"', 1)"
		cur.execute(sql)
		mysql.connection.commit()
	
		flash(f'Account created for {username}!', 'success')
		#flash(f"{sql}", 'success')

		cur.close()

	return render_template('registration.html', title='Register', form=form)

empPosition = []
epmBranch = []

class AddMaddEmployee(Form):

	#Class to define the Add Member Form
    fname = StringField('First Name', [validators.Length(min=1, max=50), validators.InputRequired()])
    lname = StringField('Last Name', [validators.Length(min=1, max=50), validators.InputRequired()])
    username = StringField('Username', [validators.InputRequired(), validators.NoneOf(values = values, message = "Username is already taken")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    salary = StringField('Salary', [validators.InputRequired()])
    position = SelectField('Position', choices = empPosition)
    branch = SelectField('Branch', choices = epmBranch)

@app.route('/addEmployee', methods = ['GET', 'POST'])
#@is_logged_in
#@is_admin
def addEmployee():

	#Clear the lists
	empPosition.clear()
	epmBranch.clear()

	#Create the list for the branch
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT branch_Name from Branch")
	b = cur.fetchall()
	for i in range(q):
	    epmBranch.append(b[i]['branch_Name'])
	
	#Create the list for the position list
	empPosition.append("Manager")
	empPosition.append("Trainer")
	empPosition.append("Receptionist")

	form = AddMaddEmployee(request.form)
	if request.method == 'POST':
		
		#Get the data from the form
		username = request.form['username']
		fname = request.form['fname']
		lname = request.form['lname']
		password = request.form['password']
		salary = request.form['salary']
		position = request.form['position']
		branch = request.form['branch']
		
		#flash(f"{username}", 'success')
		#Update logins table
		hash = sha256_crypt.hash(password)
		if position == "Manager":
			sql = "INSERT INTO logins(username, password, profile) VALUES('" +username+ "', '" +hash+ "', 1)"
		if position == "Trainer":
			sql = "INSERT INTO logins(username, password, profile) VALUES('" +username+ "', '" +hash+ "', 3)"
		if position == "Receptionist":
				sql = "INSERT INTO logins(username, password, profile) VALUES('" +username+ "', '" +hash+ "', 2)"
		
		#flash(f"{sql}", 'success')
		cur.execute(sql)
		mysql.connection.commit()

		result = cur.execute('SELECT branch_No from Branch WHERE branch_Name = %s', [branch])
		data = cur.fetchone()
		bnum = data['branch_No']

		#Update Employees Table
		sql = "INSERT INTO Employees(firstName, lastName, branch_No, position, salary, username) VALUES( '" +fname+ "', '" +lname+ "', " +str(bnum)+", '" +position+"', '"+str(salary)+"', '"+username+"')"
		cur.execute(sql)
		mysql.connection.commit()
		#flash(f"{sql}", 'success')

	return render_template("addEmployee.html", title='Add Employee', form=form);	

eqBranch = []	

class AddEquipmentForm(Form):	

	#Class to define the Add Equipment Form
    etype = StringField('Equipment Type', [validators.Length(min=1, max=50), validators.InputRequired()])
    desc = TextAreaField('Description', [validators.Length(min=1, max=50), validators.InputRequired()])
    datePur = DateField('Date Purchased', [validators.InputRequired()], format = '%m/%d/%Y')  
    branch = SelectField('Branch', choices = eqBranch) 

@app.route('/addEquipment', methods = ['GET', 'POST'])
#@is_logged_in
#@is_admin
def addEquipment():

	#Clear the lists
	eqBranch.clear()

	#Create the list for the branch
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT branch_Name from Branch")
	b = cur.fetchall()
	for i in range(q):
	    eqBranch.append(b[i]['branch_Name'])
	
	form = AddEquipmentForm(request.form)
	if request.method == 'POST':

		#Get the data from the form
		etype = request.form['etype']
		branch = request.form['branch']
		desc = request.form['desc']
		datePur = request.form['datePur']

		result = cur.execute('SELECT branch_No from Branch WHERE branch_Name = %s', [branch])
		data = cur.fetchone()
		bnum = data['branch_No']

		#Update Equipment Table
		sql = "INSERT INTO Equipment(equipment_Type, branch_No, description, date_Purchased) VALUES( '" +etype+ "', " +str(bnum)+", '" +desc+"', '"+datePur+"')"
		cur.execute(sql)
		mysql.connection.commit()
		#flash(f"{sql}", 'success')
	
	return render_template("addEquipment.html", title='Add Equipments', form=form);	

#if __name__ == "__main__":
app.run(host="0.0.0.0", port=int("5000"), debug=True)
