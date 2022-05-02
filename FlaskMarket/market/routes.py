from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages , request 
from market.models import Item, Users
from market.forms import RegisterForm, LoginForm, PurchaseItemForm , SellItemForm
from market import db
from flask_login import login_user , logout_user , login_required , current_user

@app.route('/')
def hello_world():
    return 'Hello, Faizan!'

@app.route("/about/<username>")
def about_page(username):
    return f"<h1>This is About Page of {username}</h1>"

@app.route("/home")
@app.route("/home2")
def home_page():
    return render_template('home.html')

@app.route("/market" , methods=["GET","POST"])
@login_required
def market_page():
    purchase_form=PurchaseItemForm()
    selling_form=SellItemForm()
    if request.method=="POST":
        ## Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name = purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations. You have purchased {p_item_object.name} for Rs.{p_item_object.price}")
            else:
                flash(f"Unfortunately you dont have enough money to purchase this {p_item_object.name}")
        # Sold Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name = sold_item).first() # This is grabbing the object of the Item
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user) #This Sell method should do exact opposite of the buy method
                flash(f"Congratulations! You sold {s_item_object.name} back to the market" , category="success")
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category = "danger")    
        return redirect(url_for('market_page'))        

    if request.method=="GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner = current_user.id) 
        return render_template('market.html', items=items , purchase_form=purchase_form , owned_items = owned_items , selling_form = selling_form)

@app.route("/register", methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create=Users(username=form.username.data, email_address=form.email_address.data, password=form.password1.data) #This line of code goes inside our password setter and after the function in our password setter is executed
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create) # directly login over here just after creating
        flash(f"Account is created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user:{err_msg}', category='danger')
    return render_template('register.html',form=form)


@app.route('/login', methods=["GET","POST"])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as:{attempted_user.username}', category='success')
            return redirect(url_for('market_page')) ##If we succeed we redirect user to the market page
        else:
            flash('Username and Password do not match! Please try again', category='danger')    
    return render_template('login.html', form=form)    


@app.route('/logout')
def logout_page():
    logout_user()     
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))