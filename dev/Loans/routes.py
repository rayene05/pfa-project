from dev.models import BankAccount,Loan_request,Stat
from flask import render_template, url_for, flash, redirect,session
from dev.Loans.forms import confirmLoan,simulate_loan
from dev import  db
from flask_login import (
    login_required,
    current_user,
)

from flask import Blueprint
loans=Blueprint('loans',__name__)
import pickle
import numpy as np 
import pandas as pd
# Load the model from the file
with open('C:\\Users\\ezzed\\Desktop\\siteweb\\flaskapp\\ml\\model3.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

@loans.route("/simulate_credit", methods=["GET", "POST"])
@login_required
def simulate_credit():
    simulate_form = simulate_loan()
    bank_accounts = BankAccount.query.filter_by(user_id=current_user.id).all()
    simulate_form.bank_account.choices = [(ba.account_number, ba.account_number) for ba in bank_accounts]
   
    if simulate_form.validate_on_submit():
        bank_account = simulate_form.bank_account.data
        for ba in bank_accounts:
            if ba.account_number == bank_account:
                account_id = ba.id
                client_name = ba.client_name
                backref = ba
           
        amount = simulate_form.amount.data
        duration = simulate_form.duration.data*30
        duration_time=duration/30
        interest= 0.05
        payment=((0.05*amount)+amount)/duration_time
      
         

        loan_request = Loan_request(
            account_number=bank_account, amount=amount, client_name=client_name,
            duration=duration, interest=interest, payment=payment, account_id=account_id,
            bank_account=backref
        )
        session['loan_request_details'] = {
            'account_number': bank_account,
            'amount': amount,
            'client_name': client_name,
            'duration': duration,
            'interest': interest,
            'payment': payment,
            'account_id': account_id
        }
        session['simulate_form_submitted'] = True
        return redirect(url_for("loans.confirm_loan"))
    
    return render_template("simulate_credit.html", form=simulate_form, show_modal=False)
@loans.route("/confirm_loan", methods=["GET", "POST"])
@login_required
def confirm_loan():
    if  session.get('simulate_form_submitted')==None and session.get('loan_request_details')==None :
        return redirect(url_for('loans.simulate_credit'))
    confirm_form = confirmLoan()
    session['simulate_form_submitted'] = None


    loan_request_details = session.get('loan_request_details')
    print(loan_request_details)
    loan={"Gender":current_user.Gender,
          "Married":current_user.Married,
          "Dependents":current_user.Dependents,
          "Education":current_user.Education,
          "Self_Employed":current_user.Self_Employed,
          "Credit_History":current_user.Credit_History,
          "Property_Area":current_user.Property_Area,
          "ApplicantIncomeLog":np.log(current_user.ApplicantIncome),
          "LoanAmountlog":np.log(loan_request_details['amount']),
          "LoanAmountTermlog":np.log(loan_request_details['duration']),
          "TotalIncomelog":current_user.TotalIncome,


    }
    input_df = pd.DataFrame([loan])
    loan_status = loaded_model.predict(input_df)
    print(loan_status[0])

    print('loan_request details is =',loan_request_details)
    loan_request = Loan_request(**loan_request_details)
    loan_request.resultat = str(loan_status[0])
    print(loan_request)
      
    if confirm_form.validate_on_submit():
         
            stat=Stat.query.filter_by(account_number=loan_request.account_number).first() 
            stat.nbloan=stat.nbloan+1
            db.session.add(loan_request)
            session['loan_request_details']=None
            db.session.commit()
            flash('Your loan request has been submitted!', 'success')
           
            return redirect(url_for('users.dashboard'))
            
  
    return render_template("confirm_loan.html", confirm_form=confirm_form, show_modal=True,  loan_request=loan_request)
@loans.route("/dashboard/loanResult", methods=["GET"])
@login_required
def loanResult():
    # Fetch the bank accounts for the current user
    bank_accounts= BankAccount.query.filter_by(user_id=current_user.id).all()
    loans=[]
    for ba in bank_accounts:
        for loan in ba.loan_requests:
            loan_dict = {
                'account_number': loan.account_number,
                'amount': loan.amount,
                'payment': loan.payment,
                'client_name': loan.client_name,
                'interest': loan.interest,
                'duration': loan.duration,
                'resultat': loan.resultat
            }
            loans.append(loan_dict)
            
    return render_template(
        "loanResult.html",
        title="loanResult",
        loans=loans,
        active_tab="loan_result",
    )
