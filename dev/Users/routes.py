from dev.models import User,BankAccount,Stat
from flask import render_template, url_for, flash, redirect,request
from dev.Users.forms import RegistrationForm,LoginForm,UpdateProfileForm,RequestResetForm,ResetPasswordForm
from dev import  bcrypt, db
from dev.Users.helpers import (save_picture,send_reset_email)

from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)

from flask import Blueprint
users=Blueprint('users',__name__)

@users.route('/register',methods=["GET", "POST"])
def register():

    form=RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    if form.validate_on_submit():
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
         
         user= db.session.query(User).filter(User.identifier == form.identifier.data).first()
         bank_accounts=db.session.query(BankAccount).filter(BankAccount.identifier==form.identifier.data)
         
         for bank_account in bank_accounts:  
            bank_account.user_id=user.id
            stat=Stat(account_number=bank_account.account_number,nbtransaction=0,nbloan=0)
            db.session.add(stat)
         user.username=form.username.data
         user.email=form.email.data
         user.password=hashed_password
         
       
        
         db.session.commit()
         flash("You have been logged in!", "success")
         return redirect(url_for("users.login1"))

    return render_template('register.html',form=form)
@users.route("/login1", methods=["GET", "POST"])
def login1():
     if current_user.is_authenticated:
        return redirect(url_for("users.dashboard"))
     form = LoginForm()
     if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.id==1 and bcrypt.check_password_hash(user.password, form.password.data):
             print('admin enter ')
             login_user(user, remember=form.remember.data)
             return(redirect(url_for('admin.index')))
            elif user and bcrypt.check_password_hash(user.password, form.password.data):
                print('user enter')
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash("You have been logged in!", "success")
                return redirect(next_page) if next_page else redirect(url_for("users.dashboard"))
            
            else:
                
                flash("Login Unsuccessful. Please check credentials", "danger")
     return render_template("login1.html", title="Login", form=form)
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))
@users.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard", active_tab=None)
@users.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("users.profile"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        
    image_file = url_for("static", filename=f"user_pics/{current_user.image_file}")
    return render_template(
        "profile.html",
        title="Profile",
        profile_form=profile_form,
        image_file=image_file,
        active_tab="profile",
    )
@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("users.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash(
            "If this account exists, you will receive an email with instructions",
            "info",
        )
        return redirect(url_for("users.login1"))
    return render_template("reset_request.html", title="Reset Password", form=form)
@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("The token is invalid or expired", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated. You can now log in", "success")
        return redirect(url_for("users.login1"))
    return render_template("reset_password.html", title="Reset Password", form=form)