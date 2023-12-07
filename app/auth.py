from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import app, db
from .models import User
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

# login page
@auth.route('/login')
def login():
    form=LoginForm()
    return render_template('login.html', form=form, title='Login')

# login request
@auth.route('/login', methods=['POST'])
def login_post(): 
    form=LoginForm()
    # check if form is valid
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
    # check if user exists
    user=User.query.filter_by(email=email).first()
    if not user:
        flash('Email not found. Please check this email address is correct or register if you do not have an account.')
    # check if password is correct
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect password. Please try again.')
        return redirect(url_for('auth.login'))
    # if user exists and password is correct, log in
    login_user(user)
    return redirect(url_for('ratings.user_profile'))

# logout request
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('ratings.index'))

# register page
@auth.route('/register')
def register(): 
    form=RegisterForm()
    return render_template('register.html', form=form, title='Register')

# register request
@auth.route('/register', methods=['POST'])
def register_post(): 
    form=RegisterForm()
    # check if form is valid
    if form.validate_on_submit():
        email=form.email.data
        username=form.username.data
        password=form.password.data
    # check if user exists
    user_email=User.query.filter_by(email=email).first()
    if user_email:
        flash('Email address already exists. Please choose another email address or ')
        return redirect(url_for('auth.register'))
    # check if username exists
    user_username=User.query.filter_by(username=username).first()
    if user_username:
        flash('Username already exists Please choose another username or ')
        return redirect(url_for('auth.register'))
    # if user does not exist, create new user
    new_user=User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha1', salt_length=8))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))