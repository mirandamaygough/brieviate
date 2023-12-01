# setup of views to navigate through the app
from flask import Flask, render_template, flash, redirect, request, jsonify, url_for, Blueprint
from flask_login import login_required, current_user
from app import app
from app import db
from .forms import ReviewForm
from .models import User, Cheese, Review

views = Blueprint('views', __name__)

# home page
@views.route('/')
# @login_required
def index():
    return render_template('index.html')

@views.route('/feed')
@login_required
def feed():
    reviews=Review.query.all()
    return render_template('feed.html', reviews=reviews)

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.email)

@views.route('/new_rating')
@login_required
def new_rating():
    form=ReviewForm()
    selected_rating=None
    return render_template('new_rating.html', form=form, selected_rating=selected_rating)

@views.route('/new_rating', methods=['POST'])
@login_required
def new_rating_post():
    form=ReviewForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print('hello')
        cheese=form.cheese.data
        brand=form.brand.data
        rating=form.rating.data
        review=form.review.data
        cheese_to_review=Cheese.query.filter_by(name=cheese).first()
        if not cheese_to_review:
            new_cheese=Cheese(name=cheese)
            db.session.add(new_cheese)
            db.session.commit()
            cheese_to_review=Cheese.query.filter_by(name=cheese).first()
            print(cheese_to_review.name)
        new_review=Review(cheese_id=cheese_to_review.id, user_id=current_user.id, brand=brand, rating=rating, review=review)
        db.session.add(new_review)
        db.session.commit()
    return redirect(url_for('views.feed'))