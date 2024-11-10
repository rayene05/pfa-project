
from dev.models import BankAccount,Transaction
from flask import render_template
from datetime import  date
from dev import db

from flask_login import (
    login_required,

    current_user,
   
    login_required,
)
from sqlalchemy import func

from flask import Blueprint
bankaccounts_bp=Blueprint('bankaccounts',__name__)
@bankaccounts_bp.route("/dashboard/choose_bank_account", methods=["GET", "POST"])
@login_required
def choose_bank_account():
    # Fetch the bank accounts for the current user
    today = date.today()
    
    
    bank_accounts = BankAccount.query.filter_by(user_id=current_user.id).all()
    for account in bank_accounts:
        if account.upcomming:
            if account.upcomming_date.date()!=today:
                print(today)
                print(account.upcomming_date)
                account.upcomming=None
    db.session.commit()
    years = today.year
    month=today.month
    return render_template(
        "choose_bank_account.html",
        title="Choose Bank Account",
        bank_accounts=bank_accounts,
        active_tab="choose_bank_account",
        years=years,
        month=month

    )

