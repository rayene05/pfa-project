from flask_wtf import FlaskForm


from wtforms import  SubmitField,SelectField,FloatField,IntegerField
from wtforms.validators import DataRequired,NumberRange


class simulate_loan(FlaskForm):
    
    bank_account = SelectField("Acount_Number", choices=[])
    
    amount = FloatField("Amount", validators=[DataRequired(), NumberRange(min=100, max=200000)])
    duration = IntegerField("Duration ", validators=[DataRequired()])
    submit = SubmitField("simulate")

class confirmLoan(FlaskForm):
      submit = SubmitField("confirm")
