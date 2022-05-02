from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) # Creating an Instance
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY']='6f9c0a5aba23b260a3186891'
login_manager.login_view="login_page" 
login_manager.login_message_category="info" #Tells that we want to display the message in information form

from market import routes




