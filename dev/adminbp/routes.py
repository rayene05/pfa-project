from flask import Blueprint,render_template,session,jsonify
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from dev import admin, db, bcrypt
from sqlalchemy import func,extract
from datetime import datetime
from dev.models import User, BankAccount, Transaction,Loan_request,Stat
from flask_admin import AdminIndexView,Admin
from flask_admin import AdminIndexView, expose
import json
adminbp = Blueprint("adminbp", __name__)

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1
class statview(ModelView):
    @expose('/')
    def index(self):
        loans_per_months = []
        months=[]
        nb_user = db.session.query(func.count(Stat.id)).scalar()
        nb_client = db.session.query(func.count(User.id)).scalar()
        current_year = datetime.now().year
        nbtransaction_18 = db.session.query(func.count(Transaction.id)).join(BankAccount).filter(BankAccount.age_of_user.between(18, 30)).scalar()
        nbtransaction_30 = db.session.query(func.count(Transaction.id)).join(BankAccount).filter(BankAccount.age_of_user.between(31, 40)).scalar()
        nbtransacion_40 = db.session.query(func.count(Transaction.id)).join(BankAccount).filter(BankAccount.age_of_user.between(41, 60)).scalar()
        
        nbtransaction_60 = db.session.query(func.count(Transaction.id)).join(BankAccount).filter(BankAccount.age_of_user.between(61, 200)).scalar()
        loans_per_month = db.session.query(extract('month', Loan_request.date), func.count(Loan_request.id)).filter(extract('year', Loan_request.date) == current_year).group_by(extract('month', Loan_request.date)).all()
        print(loans_per_month)
        
        for month, count in loans_per_month:
            loans_per_months.append(count)
            months.append((month))

        print('**************')
        print(loans_per_months)
        print('month=')
        print(months)
        print(nbtransaction_30)

        return self.render('admin/stat.html', loans_per_months=loans_per_months,months=months,nbtransaction_18=nbtransaction_18,nbtransacion_40=nbtransacion_40,nbtransaction_60=nbtransaction_60,nbtransaction_30=nbtransaction_30,nb_client=nb_client,nb_user=nb_user)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1


   
     
    
class transactionview(ModelView) :
    form_columns=['date' ,  'description', 'amount', 'account_id','accont_reciver','account_number','status' ]
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1
class userview(ModelView) :
    
    TotalIncome=db.Column(db.Integer)
    form_columns=['id' ,'password','fname' ,'lname' ,'identifier','PersonalCode','Gender','Married','Dependents','Education','Credit_History','Property_Area','ApplicantIncome','TotalIncome','Self_Employed']
    def on_model_change(self, form, model, is_created):
     if form.password.data:
        model.password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8)"
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1
class bankview(ModelView):
    form_columns=['account_number','identifier','balance','creation_date','account_type','client_name']
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1
  




# Register the custom view
 
admin.add_view(userview(User, db.session, menu_icon_type='fa', menu_icon_value='fa-user'))
admin.add_view(statview(
    Stat,
    db.session,
    menu_icon_type='fa',  # Use FontAwesome icons
    menu_icon_value='fa-flask',  # Specify the icon name (e.g., 'fa-flask')
    endpoint='stat'  # Your endpoint
))
admin.add_view(bankview(BankAccount, db.session, menu_icon_type='fa', menu_icon_value='fa-university'))
admin.add_view(transactionview(Transaction, db.session, menu_icon_type='bi', menu_icon_value='bi-arrow-down-up'))
admin.add_view(MyModelView(Loan_request, db.session, menu_icon_type='fa', menu_icon_value='fa-credit-card'))

