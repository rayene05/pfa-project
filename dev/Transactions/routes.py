from dev.models import BankAccount,Transaction,Stat
from flask import render_template, url_for, redirect,abort,flash
from dev.Transactions.forms import FilterForm,TransactionForm
from dev import db 
from datetime import date

from flask_login import (
    login_required,
    
    current_user,
    
)
from sqlalchemy import func
from flask import Blueprint
transactions_bp=Blueprint('transactions_bp',__name__)
@transactions_bp.route("/display_account/<uuid>/<month>/<years>", methods=["GET", "POST"])
@login_required
def display_account(uuid, month, years):
    form = FilterForm()  
    
    if form.validate_on_submit():
        new_month = form.month.data
        new_years=form.years.data
        return redirect(url_for('transactions_bp.display_account', uuid=uuid, month=new_month, years=new_years))

    account = BankAccount.query.filter_by(uuid=uuid).first()
    if account.user_id != current_user.id:
        abort(403)
    print(month)
   
   
    if month and years :
        
        transactions = Transaction.query.filter( 
        Transaction.account_id == account.id, 
        func.extract('year', Transaction.date) == int(years),
        func.extract('month', Transaction.date) == int(month)
    ).all()
        tran= Transaction.query.filter( 
        Transaction.accont_reciver == account.account_number, 
        func.extract('year', Transaction.date) == int(years),
        func.extract('month', Transaction.date) == int(month)
    ).all()
        
    print(tran)
    print(transactions)
    
    form.month.label.text = "Month: " + str(month)
    form.years.label.text = "Year: " + str(years)
    

    return render_template(
        "display_account.html",
        title="Account Details",
        transactions=transactions,
        tran=tran,
        form=form,
        month=month,  # Pass the month to the template
        years=years

    )
@transactions_bp.route('/dashboard/send_transaction',methods=['GET', 'POST'])
def send_transaction():
    form= TransactionForm()
    bank_accounts = BankAccount.query.filter_by(user_id=current_user.id).all()
    form.bank_account.choices = [(ba.account_number, ba.account_number) for ba in bank_accounts]
    if form.validate_on_submit():
        bank_sender= BankAccount.query.filter_by(account_number=form.bank_account.data).first()
        bank_reciver=BankAccount.query.filter_by(account_number=form.account_reciver.data).first()
        
        # Check if sender and receiver are not the same
        if bank_sender != bank_reciver:
            transaction=Transaction(account_number=form.bank_account.data,
            description=form.description.data,
            accont_reciver=form.account_reciver.data,
            amount=form.amount.data,account_id =BankAccount.query.filter_by(account_number=form.bank_account.data).first().id)
            db.session.add(transaction)
            
            bank_sender.balance=bank_sender.balance-form.amount.data
            current_date = date.today()
            bank_reciver.upcomming_date=current_date
            upcomming=db.session.query(func.sum(Transaction.amount)).filter(Transaction.date == current_date,Transaction.accont_reciver==form.account_reciver.data).scalar()
            if upcomming:
                bank_reciver.upcomming=upcomming
            bank_reciver.balance=bank_reciver.balance+form.amount.data
            stat=Stat.query.filter_by(account_number=form.bank_account.data).first() 
            stat.nbtransaction=stat.nbtransaction+1
            db.session.commit()
            flash(f"ur money is sended have good time at our bank","success")
            
            return redirect(url_for('users.dashboard'))
        else:
            flash(f"Sender and receiver cannot be the same account","danger")
    
    return render_template('send_transaction.html',form=form)
