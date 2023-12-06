from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import app, db
from .models import User
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    form=LoginForm()
    return render_template('login.html', form=form)

@auth.route('/login', methods=['POST'])
def login_post(): 
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
    user=User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user)
    return redirect(url_for('ratings.user_profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('ratings.index'))

@auth.route('/register')
def register(): 
    form=RegisterForm()
    return render_template('register.html', form=form)

@auth.route('/register', methods=['POST'])
def register_post(): 
    form=RegisterForm()
    if form.validate_on_submit():
        email=form.email.data
        username=form.username.data
        password=form.password.data
    user=User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.register'))
    new_user=User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha1', salt_length=8))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))