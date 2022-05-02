from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,SubmitField,BooleanField
#BooleanField is basically for true and false and used for remenber entry in login form
#SubmitField is used to submit form 
##This is for making forms with name as an input field and as name is string so StringField
#The Password field is for password entry
from wtforms.validators import DataRequired,Length,Email,EqualTo
#EqualTo validator is used to check whther the password and confirmation both are equal
#This DataRequired is imported to make sure that no field is empty
##This Length validator is there to restrict the length of our data entry
##Email validator is used to check whether our email entry is valid or not

class RegistrationForm(FlaskForm): #This will Inherit from FlaskFrom
	username=StringField('Username', validators=[DataRequired(),
	Length(min=2,max=20)])#The validators will be a list of checks which we want to put
	#StringField denotes that our data entry has to be in String
	#'username' is basically going to be a label 
	email=StringField('Email', validators=[DataRequired(),
		Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password', validators=[DataRequired(),
		EqualTo('password')]) # The argument in EqualTo will be the field with which we want it to be equal
	submit=SubmitField('Sign Up')


class LoginForm(FlaskForm): #This we are creating our login form
	email=StringField('Email', validators=[DataRequired(),
		Email()])
	password=PasswordField('Password',validators=[DataRequired()])
	remember=BooleanField('Remember Me') #This is for staying logged in for some time 
	submit=SubmitField('Login')







	
