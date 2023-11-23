# setup of views to navigate through the app
from flask import Flask, render_template, flash, redirect, request, jsonify, url_for
from app import app
from flask_security import login_required, current_user
from flask_login import login_user, logout_user
from app import db
# from .forms import IncomeForm, ExpensesForm, GoalForm
from .models import User

# home page
@app.route('/')
@login_required
def index():
    return "cheese app"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Create a new user object
        new_user = User(email=email, password=User.set_password(password))
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
    