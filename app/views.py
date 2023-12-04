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
    reviews_original=Review.query.all()
    reviews=[]
    for entry in reviews_original:
        review={}
        review['cheese']=Cheese.query.filter_by(id=entry.cheese_id).first().name
        review['user']=User.query.filter_by(id=entry.user_id).first().username
        review['brand']=entry.brand
        review['rating']=entry.rating
        review['review']=entry.review
        reviews.append(review)
    return render_template('feed.html', reviews=reviews)

@views.route('/profile')
@login_required
def profile():
    reviews_original = Review.query.filter_by(user_id=current_user.id).all()
    reviews = []
    for entry in reviews_original:
        review = {}
        review['id']=entry.id
        review['cheese'] = Cheese.query.filter_by(id=entry.cheese_id).first().name
        review['brand'] = entry.brand
        review['rating'] = entry.rating
        review['review'] = entry.review
        reviews.append(review)
    return render_template('profile.html',  reviews=reviews)

@views.route('/user/<username>/reviews')
@login_required
def user_reviews(username):
    user=User.query.filter_by(username=username).first()
    reviews_original = Review.query.filter_by(user_id=user.id).all()
    reviews = []
    for entry in reviews_original:
        review = {}
        review['cheese'] = Cheese.query.filter_by(id=entry.cheese_id).first().name
        review['brand'] = entry.brand
        review['rating'] = entry.rating
        review['review'] = entry.review
        reviews.append(review)
    return render_template('user_reviews.html', username=username, reviews=reviews)

@views.route('/new_rating')
@login_required
def new_rating():
    form=ReviewForm()
    selected_rating=0
    return render_template('new_rating.html', form=form, selected_rating=selected_rating)

@views.route('/new_rating', methods=['POST'])
@login_required
def new_rating_post():
    form=ReviewForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        try:
            cheese=form.cheese.data
            brand=form.brand.data
            rating=form.rating.data
            review=form.review.data
            cheese_to_review=Cheese.query.filter_by(name=cheese).first()
            new_review=Review(cheese_id=cheese_to_review.id, user_id=current_user.id, brand=brand, rating=rating, review=review)
            db.session.add(new_review)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('views.feed'))

@views.route('/edit_rating_handler', methods=['GET', 'POST'])
@login_required
def edit_rating_handler():
    if request.method=='GET':
        id=request.args.get('id')
        return redirect(url_for('views.edit_rating', id=id))
    else:
        form=ReviewForm()
        id=request.args.get('id')
        try:
            review_to_edit=Review.query.filter_by(id=id).first()
            review_to_edit.cheese=form.cheese.data
            review_to_edit.cheese_id=Cheese.query.filter_by(name=form.cheese.data).first().id
            review_to_edit.brand=form.brand.data
            review_to_edit.rating=form.rating.data
            review_to_edit.review=form.review.data
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return redirect(url_for('views.profile'))

@views.route('/edit_rating', methods=['GET'])
@login_required
def edit_rating():
    id=request.args.get('id')
    review_to_edit=Review.query.filter_by(id=id).first()
    form=ReviewForm()
    form.cheese.default=Cheese.query.filter_by(id=review_to_edit.cheese_id).first().name
    form.brand.default=review_to_edit.brand
    selected_rating=review_to_edit.rating
    form.review.default=review_to_edit.review
    form.process()
    return render_template('edit_rating.html', form=form, id=id, selected_rating=selected_rating)