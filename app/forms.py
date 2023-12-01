# setup for income and expenses forms
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Email

class LoginForm(FlaskForm):
    email = StringField('Email', default='', validators=[InputRequired(), Email()])
    password= PasswordField('Password', default='', validators=[InputRequired()])
    submit = SubmitField('Submit')
    
class RegisterForm(FlaskForm):
    email = StringField('Email', default='', validators=[InputRequired(), Email()])
    username = StringField('Username', default='', validators=[InputRequired()])
    password= PasswordField('Password', default='', validators=[InputRequired()])
    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
    cheese = StringField('Cheese', default='', validators=[InputRequired()])
    brand = StringField('Brand', default='', validators=[InputRequired()])
    rating = IntegerField('Rating', default=0)
    review = StringField('Review', default='', validators=[InputRequired()])
    submit = SubmitField('Submit')