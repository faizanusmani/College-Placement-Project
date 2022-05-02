from datetime import datetime
from flask import Flask,render_template, url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm #from forms.py we are importing classes for Login and registration form into our program
 #This render_template function is used to import html pages which we want to render in our app or website
app = Flask(__name__)  ## This is how we create a flask app which is our website

app.config['SECRET_KEY']='cc2468d7e9ea75f0c9d0cc18ffd1178c'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', lazy = True)

def __repr__(self):
	return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.String(20), primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def __repr__(self):
	return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author': 'Faizan Usmani',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 28, 2021'
    },
    {
        'author': 'Faza Eliza Usmani',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'May 1, 2021'
    }
]



@app.route("/")##Routes are what we type into browsers to go into different pages. This "/" is the home page of our website
@app.route("/home") #This will setup 2 routes for the same function
def home():
	return render_template('home.html',posts=posts) #Now we will use this posts on the left side variable in our template

@app.route("/about")
def about():
	return render_template('about.html',title='About')

@app.route("/register",methods=['GET','POST'])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!','success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login",methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		if form.email.data=='faizanusmani248@gmail.com' and form.password.data=='qwerty123':
			flash('You have been logged In!','success')
			return redirect(url_for('home'))
		else:
		    flash('Login Unsuccessful.','danger') #danger is bootstrap class for alert	
	return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':   
	app.run(debug=True)

