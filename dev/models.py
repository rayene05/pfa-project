from dev import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
import uuid
from itsdangerous import URLSafeTimedSerializer as Serializer
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=True)
    email = db.Column(db.String(125), unique=True, nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(60), nullable=False)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    identifier = db.Column(db.Integer, unique=True, nullable=False)
    PersonalCode = db.Column(db.Integer, unique=True, nullable=True)
    Gender=db.Column(db.Integer)
    Married=db.Column(db.Integer)
    Dependents=db.Column(db.Integer)
    Education=db.Column(db.Integer)
    Credit_History=db.Column(db.Float)
    Property_Area=db.Column(db.Integer)
    ApplicantIncome=db.Column(db.Float)
    TotalIncome=db.Column(db.Float)
    Self_Employed=db.Column(db.Integer)
 
    bank_accounts = db.relationship('BankAccount', backref='user', lazy=True)
    
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, age=3600):
        s = Serializer(current_app.config['SECRET_KEY'], salt='pw-reset')
        try:
            user_id = s.loads(token, max_age=age)['user_id']
        except:
            return None
        return User.query.get(user_id)

   
    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}', '{self.image_file}')"
class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid=db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    identifier = db.Column(db.Integer,  nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    client_name = db.Column(db.String(25), nullable=False)
    transactions = db.relationship('Transaction', backref='bank_account', lazy=True)
    loan_requests = db.relationship('Loan_request', backref='bank_account', lazy=True)
    upcomming=db.Column(db.Float,default=0)
    upcomming_date= db.Column(db.DateTime) 
    age_of_user= db.Column(db.Integer)
   
    def __repr__(self):
        return f"BankAccount('{self.account_number}', '{self.balance}', '{self.creation_date}', '{self.account_type}')"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    accont_reciver= db.Column(db.String(20), nullable=False)
    account_number=db.Column(db.String(20), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable=False)
   
    status=db.Column(db.String,default="not affected")

    def __repr__(self):
        return f"Transaction('{self.date}', '{self.description}', '{self.amount}')"
class Loan_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    client_name = db.Column(db.String(25), nullable=False)
    interest = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    payment = db.Column(db.Float, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable=False)
    date=   date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    resultat = db.Column(db.String, default="approved")

    def __repr__(self):
        return f"('{self.account_number}', '{self.amount}','{self.client_name}','{self.interest}','{self.duration}','{self.payment}')"
class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    nbtransaction=db.Column(db.Integer)
    nbloan=db.Column(db.Integer)
   