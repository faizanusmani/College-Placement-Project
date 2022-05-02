from market import db, login_manager
from market import bcrypt ## We Initialized it in our init file
from flask_login import UserMixin #This class contains the 4 methods required for login system


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref = 'owned_user', lazy = True)

    @property
    def prettier_budget(self):
        if len(str(self.budget))>=4:
            return f'Rs.{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f"{self.budget}"

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_text_password):     #Here we will receive actual password entered by the user
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') #This generate_password_hash will receive a plain-text-password as an argument. UTF-8 is used to decode the password hash
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price  

    def can_sell(self, item_obj):
        return item_obj in self.items  # Will return true if the current user has those Items

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit() # To save this action in our database    

    def sell(self, user):
        self.owner = None # Assign the ownership to nobody
        user.budget += self.price
        db.session.commit()

