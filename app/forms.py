# setup for income and expenses forms
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Email
from app import app
from app import db
from .models import Cheese

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
    choices=[]
    @staticmethod
    def get_cheeses():
        with app.app_context():
            cheeses = [(cheese.name) for cheese in Cheese.query.all()]
            return cheeses
    cheese = SelectField('Select a Cheese', choices=get_cheeses(), validators=[InputRequired()])
    brand = StringField('Brand', default='', validators=[InputRequired()])
    rating = IntegerField('Rating', default=0)
    review = TextAreaField('Review', default='', validators=[InputRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.choices = self.get_cheeses()

class ReviewFilterForm(FlaskForm):
    filter_option = SelectField('Filter by: ', choices=[('newest-first', 'Newest first'), ('oldest-first', 'Oldest first'), ('highest-rated', 'Highest rated'), ('lowest-rated', 'Lowest rated'), ('most-liked', 'Most liked')], default='newest-first')
    submit = SubmitField('Go')
