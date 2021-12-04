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
app.config['MYSQL_HOST'] = 'csc540_project_db_1'
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

#function to determin if the logged in user is a employee.
def is_employee(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session['profile'] == 3:
			return f(*args, **kwargs)
		elif session['profile'] == 1:
			return f(*args, **kwargs)
		elif session['profile'] <= 2:
			return f(*args, **kwargs)
		else:
			flash('You are not a employee!!, You do not have access to this page.', 'danger')
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

#Form for changing user password
class ChangePasswordForm(Form):
	old_password = PasswordField('Existing Password')
	new_password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message = 'Passwords do not match!')
	])
	confirm = PasswordField('Confirm Password')

#Route and function for changing user password
@app.route('/update_password/<string:username>', methods = ['GET', 'POST'])
def update_password(username):
	
	form = ChangePasswordForm(request.form)
	if request.method == 'POST' and form.validate():
		new = form.new_password.data
		entered = form.old_password.data

		#getting current password from the database
		cur = mysql.connection.cursor()
		cur.execute("SELECT password FROM logins WHERE username = %s", [username])
		old = (cur.fetchone())['password']

		#IF the old password entered matches the db then update db with the new password
		if sha256_crypt.verify(entered, old):
			cur.execute("UPDATE logins SET password = %s WHERE username = %s", (sha256_crypt.encrypt(new), username))
			mysql.connection.commit()
			cur.close()
			flash('New password will be in effect from next login!!', 'info')
			return redirect(url_for('memberDashboard', username = session['username']))
		
		cur.close()
		flash('Old password you entered is not correct!!, try again', 'warning')

	return render_template('updatePassword.html', form = form)

#Route and Function for adminDashboard
@app.route('/adminDashboard')
@is_logged_in
@is_admin
def adminDashboard():
    return render_template("adminDashboard.html"); 

#Route and Function for trainerDashboard
@app.route('/trainerDashboard')
@is_logged_in
@is_trainer
def trainerDashboard():
    return render_template("trainerDashboard.html"); 

#Route and Function for receptionistDashboard
@app.route('/receptionistDashboard')
@is_logged_in
@is_recep_level
def receptionistDashboard():
    return render_template("receptionistDashboard.html"); 

#Route and Function for memberDashboard
@app.route('/memberDashboard/<string:username>')
@is_logged_in
def memberDashboard(username):
    return render_template('memberDashboard.html')

#Route and Function for logout function
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))

#List and addMember form for member registration
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

#Route and function for member registration.
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

class addEmployeeForm(Form):

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

#Route and function for addEmployee
@app.route('/addEmployee', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
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

	form = addEmployeeForm(request.form)
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
		flash(f'You created a new employee {username}!!', 'success')
		return redirect(url_for('adminDashboard'))
		

	return render_template("addEmployee.html", title='Add Employee', form=form);	

delEmp = []

class DeleteEmployeeForm(Form):
	username = SelectField(u'Choose Employee to delete', choices=delEmp)

@app.route('/DeleteEmployee', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def DeleteEmployee():
	delEmp.clear()
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT username FROM Employees")
	b = cur.fetchall()

	for i in range(q):
		tup = (b[i]['username'],b[i]['username'])
		delEmp.append(tup)

	form = DeleteEmployeeForm(request.form)
	if len(delEmp)==1:
		flash('You cannot remove your only Employee!!', 'danger')
		return redirect(url_for('adminDashboard'))
	
	if request.method == 'POST':
		username = form.username.data
		
		cur.execute("DELETE FROM Employees WHERE username = %s", [username])
		cur.execute("DELETE FROM logins WHERE username = %s", [username])
		
		mysql.connection.commit()
		cur.close()
		delEmp.clear()
		flash(f'You removed your employee {username}!!', 'success')
		return redirect(url_for('adminDashboard'))

	return render_template('DeleteEmployee.html', form = form)

eqBranch = []	

class AddEquipmentForm(Form):	

	#Class to define the Add Equipment Form
    etype = StringField('Equipment Type', [validators.Length(min=1, max=50), validators.InputRequired()])
    desc = TextAreaField('Description', [validators.Length(min=1, max=50), validators.InputRequired()])
    datePur = DateField('Date Purchased', [validators.InputRequired()], format = '%m/%d/%Y')  
    branch = SelectField('Branch', choices = eqBranch) 

@app.route('/addEquipment', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
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
		flash(f'You added new equipment to the {branch} branch!!', 'success')
		return redirect(url_for('adminDashboard'))
	
	return render_template("addEquipment.html", title='Add Equipments', form=form);	

delEqu = []

class DeleteEquipmentForm(Form):
	equipment = SelectField(u'Choose Equipment to delete', choices=delEqu)

@app.route('/DeleteEquipment', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def DeleteEquipment():
	delEqu.clear()
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT equipment_Type FROM Equipment")
	b = cur.fetchall()

	for i in range(q):
	    delEqu.append(b[i]['equipment_Type'])

	form = DeleteEquipmentForm(request.form)
	
	if request.method == 'POST':
		equipment = form.equipment.data
		
		cur.execute("DELETE FROM Equipment WHERE equipment_Type = %s", [equipment])
		
		mysql.connection.commit()
		cur.close()
		delEqu.clear()
		flash(f'You removed your Equipment!!', 'success')
		return redirect(url_for('adminDashboard'))

	return render_template('DeleteEquipment.html', form = form)

@app.route('/viewMyClasses', methods = ['GET', 'POST'])
@is_logged_in
@is_employee
def viewMyClasses():

	cur = mysql.connection.cursor()
	sql = """SELECT class_name, class_type, date_start, time_start FROM Classes
    ORDER BY date_start;"""
	cur.execute(sql)
	
	#cur.execute("SELECT equipment_type, description, date_Purchased, Branch_Name, address, city from Equipment NATURAL JOIN Branch;")
	data = cur.fetchall()
	#flash(f'{data}', 'success')
	return render_template('viewMyClasses.html', data = data)


@app.route('/viewEquipmentReport', methods = ['GET', 'POST'])
@is_logged_in
@is_employee
def viewEquipmentReport():

	cur = mysql.connection.cursor()
	sql = """SELECT equipment_type, description, date_Purchased, Branch_Name, address, city from Equipment 
    NATURAL JOIN Branch;"""
	cur.execute(sql)
	
	#cur.execute("SELECT equipment_type, description, date_Purchased, Branch_Name, address, city from Equipment NATURAL JOIN Branch;")
	data = cur.fetchall()
	#flash(f'{data}', 'success')
	return render_template('viewEquipmentReport.html', data = data)

@app.route('/viewMemberReport', methods = ['GET', 'POST'])
@is_logged_in
@is_employee
def viewMemberReport():

	cur = mysql.connection.cursor()
	#sql = """SELECT Customers.firstName, Customers.lastName, Customers.age, Customers.gender, Customers.Address, Customers.city, Customers.zipCode, Customers.membership_type, Branch.branch_Name FROM Customers
    # INNER JOIN Branch
    # ON Customers.branch_No = Branch.branch_No;"""

	sql = """SELECT Customers.firstName, Customers.lastName, Customers.age, 
    Customers.gender, Customers.Address, Customers.city, Customers.zipCode, 
    Customers.membership_type, Branch.branch_Name FROM Customers
     INNER JOIN Branch
     ON Customers.branch_No = Branch.branch_No;"""
	
	cur.execute(sql) 
	data = cur.fetchall()
	#flash(f'{data}', 'success')
	return render_template('viewMemberReport.html', data = data)

@app.route('/viewEmployeeReport', methods = ['GET', 'POST'])
@is_logged_in
@is_employee
def viewEmployeeReport():

	cur = mysql.connection.cursor()
	#sql = """SELECT Employees.firstName, Employees.lastName, Employees.position, Employees.salary, Branch.branch_Name FROM Employees
    # INNER JOIN Branch
    # ON Employees.branch_No = Branch.branch_No;"""

	sql = """SELECT Employees.firstName, Employees.lastName, Employees.position, 
    Employees.salary, Branch.branch_Name FROM Employees
     INNER JOIN Branch
     ON Employees.branch_No = Branch.branch_No;"""

	cur.execute(sql) 
	data = cur.fetchall()
	#flash(f'{data}', 'success')
	return render_template('viewEmployeeReport.html', data = data)

class AddBranchForm(Form):	

	#Class to define the Add Equipment Form
	bname = StringField('Branch Name', [validators.Length(min=1, max=50), validators.InputRequired()])
	address = StringField('Address', [validators.Length(min=1, max=50), validators.InputRequired()])
	city = StringField('City', [validators.Length(min=1, max=50), validators.InputRequired()])
	zipCode = StringField('Zip Code', [validators.Length(min=1, max=50), validators.InputRequired()])
	phoneNum = StringField('Phone Number', [validators.Length(min=1, max=50), validators.InputRequired()])


@app.route('/addBranch', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def addBranch():
	
	form = AddBranchForm(request.form)
	if request.method == 'POST':

		#Get the data from the form
		bname = request.form['bname']
		address = request.form['address']
		city = request.form['city']
		zipCode = request.form['zipCode']
		phoneNum = request.form['phoneNum']

		cur = mysql.connection.cursor()

		#Update Equipment Table
		sql = "INSERT INTO Branch(branch_Name, address, city, zipCode, phoneNum) VALUES( '" +bname+ "', '" +address+"', '" +city+"', '"+zipCode+"', '"+phoneNum+"')"
		cur.execute(sql)
		mysql.connection.commit()
		#flash(f"{sql}", 'success')
		flash(f'You created a new branch!!', 'success')
		return redirect(url_for('adminDashboard'))
	
	return render_template("addBranch.html", title='Add Branch', form=form);	


classType = []
classTimes = []
classbranch = []
classInstructor = []

class AddClassForm(Form):	

	#Class to define the Add Equipment Form
	  
	branch = SelectField('Branch', choices = classbranch)
	instructor = SelectField('Instructor', choices = classInstructor)
	desc = TextAreaField('Description', [validators.Length(min=1, max=250), validators.InputRequired()])
	ctype = SelectField('Class Type', choices = classType)
	ctime = SelectField('Class Time', choices = classTimes)
	cdate = DateField('Class Date', [validators.InputRequired()], format = '%m/%d/%Y')
	cname = StringField('Class Name', [validators.Length(min=1, max=25), validators.InputRequired()])
	slots = StringField('Available Slots', [validators.Length(min=1, max=2), validators.InputRequired()])


@app.route('/addClass', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def addClass():

	classType.clear()
	classTimes.clear()
	classbranch.clear()
	classInstructor.clear()

	#Create the list for the branch
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT branch_Name from Branch")
	b = cur.fetchall()
	for i in range(q):
	    classbranch.append(b[i]['branch_Name'])

	#Create the list for the Instructors
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT username from Employees WHERE position = 'Trainer' ")
	b = cur.fetchall()
	for i in range(q):
	    classInstructor.append(b[i]['username'])

	#Create the list for class types
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT class_Type from ClassTypes")
	b = cur.fetchall()
	for i in range(q):
	    classType.append(b[i]['class_Type'])

	#Create the list for class times
	cur = mysql.connection.cursor()
	q = cur.execute("SELECT class_Times from ClassTimes")
	b = cur.fetchall()
	for i in range(q):
	    classTimes.append(b[i]['class_Times'])


	form = AddClassForm(request.form)
	if request.method == 'POST':

		#Get the data from the form
		cname = request.form['cname']
		ctype = request.form['ctype']
		tstart = request.form['ctime']
		dstart = request.form['cdate']
		slots = request.form['slots']
		branch = request.form['branch']
		desc = request.form['desc']
		instructor = request.form['instructor']

		cur = mysql.connection.cursor()
		result = cur.execute('SELECT branch_No from Branch WHERE branch_Name = %s', [branch])
		data = cur.fetchone()
		branchNum = data['branch_No']

		#Update Equipment Table
		sql = "INSERT INTO Classes(instructor_ID, branch_No, class_name, class_type, class_desc, time_start, date_start, available_slots) VALUES( 1, " +str(branchNum)+", '" +cname+"', '" +ctype+"', '"+desc+"', '"+tstart+"', '"+dstart+"', "+slots+")"
		cur.execute(sql)
		mysql.connection.commit()
		#flash(f"{sql}", 'success')
		flash(f'You created a new class at the {branch} branch!!', 'success')
		return redirect(url_for('adminDashboard'))
	
	return render_template("addClass.html", title='Add New Class', form=form);

@app.route('/viewMyClassesMember', methods = ['GET', 'POST'])
@is_logged_in
def viewMyClassesMember():


	cur = mysql.connection.cursor()
	sql = """SELECT equipment_type, description, date_Purchased, Branch_Name, address, city from Equipment 
    NATURAL JOIN Branch;"""
	cur.execute(sql)
	
	data = cur.fetchall()
	#flash(f'{data}', 'success')
	return render_template('viewMyClassesMember.html', data = data)

@app.route('/viewMyAppMember', methods = ['GET', 'POST'])
@is_logged_in
def viewMyAppMember():

	
	cur = mysql.connection.cursor()
	sql = """SELECT equipment_type, description, date_Purchased, Branch_Name, address, city from Equipment 
    NATURAL JOIN Branch;"""
	cur.execute(sql)
	
	data = cur.fetchall()
	#flash(f'{data}', 'success')
	return render_template('viewMyAppMember.html', data = data)

@app.route('/registerForClasses', methods = ['GET', 'POST'])
@is_logged_in
def registerForClasses():

	
	cur = mysql.connection.cursor()
	sql = """SELECT equipment_type, description, date_Purchased, Branch_Name, address, city from Equipment 
    NATURAL JOIN Branch;"""
	cur.execute(sql)
	
	data = cur.fetchall()
	#flash(f'{data}', 'success')
	return render_template('registerForClasses.html', data = data)

app.run(host="0.0.0.0", port=int("5000"), debug=True)
