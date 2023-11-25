# setup of views to navigate through the app
from flask import Flask, render_template, flash, redirect, request, jsonify, url_for, Blueprint
from app import app
from flask_login import login_required, current_user
# from flask_login import login_user, logout_user
from app import db
# from .forms import IncomeForm, ExpensesForm, GoalForm
from .models import User

views = Blueprint('views', __name__)

# home page
@views.route('/')
# @login_required
def index():
    return render_template('index.html')
    # user=current_user
    # return "hello", user.username

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.email)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     if form.validate_on_submit():
#         user=form.user
#         login_user(user)
#         flash('Login successful.', 'success')
#         return redirect(url_for('index'))
#     form=LoginForm()
#     return render_template('login.html', form=form)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     if form.validate_on_submit():
#         user_datastore.create_user(email=form.email.data, username=form.username.data, password=form.password.data)
#         db.session.commit()
#         flash('Registration successful. Please login.', 'success')
#         return redirect(url_for('login'))
#     form=RegisterForm()
#     return render_template('register.html', form=form)
    