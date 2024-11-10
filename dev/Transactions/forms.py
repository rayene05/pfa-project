
from flask_wtf import FlaskForm
from dev import db
from dev.models import BankAccount


from wtforms import  SubmitField,SelectField,IntegerField,FloatField,StringField,ValidationError
from wtforms.validators import DataRequired,NumberRange,Length

 
class FilterForm(FlaskForm):
    month_choices = [(str(i).zfill(2), name) for i, name in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], 1)]
    month = SelectField('Enter month', choices=month_choices, validators=[DataRequired()])
    years = IntegerField('Enter years', validators=[DataRequired(), NumberRange(min=1900, max=2099)])
    submit = SubmitField('Filter')

class TransactionForm(FlaskForm):
    description = StringField("Description", validators=[DataRequired()])
    bank_account = SelectField("Acount_Number", choices=[])
    account_reciver=StringField("enter ur account reciver",validators=[DataRequired(),Length(max=20,min=20)])
    amount = FloatField("Amount", validators=[DataRequired(), NumberRange(min=100, max=200000)])
    submit = SubmitField('send')

    def validate_account_reciver(self, field):
        # Query the database for the account number
        account_exists = BankAccount.query.filter_by(account_number=field.data).first()
        if not account_exists:
            raise ValidationError("Receiver account does not exist in the database.")


    
        