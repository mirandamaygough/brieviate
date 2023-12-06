# setup of ratings to navigate through the app
from flask import Flask, render_template, flash, redirect, request, jsonify, url_for, Blueprint
from flask_login import login_required, current_user
from datetime import datetime
from app import app
from app import db
from .forms import ReviewForm, ReviewFilterForm
from .models import User, Cheese, Review

ratings = Blueprint('ratings', __name__)

# home page
@ratings.route('/')
# @login_required
def index():
    return render_template('index.html')

@ratings.route('/all_ratings')
@login_required
def all_ratings():
    review_filter_form=ReviewFilterForm()
    reviews_original=[]
    if request.method == 'GET' and 'submit' in request.args:
        selected_option = request.args.get('filter_option')
        review_filter_form.filter_option.default = selected_option
        review_filter_form.process()
    else:
        selected_option = 'newest-first'
    if selected_option == 'newest-first':
        reviews_original = Review.query.order_by(Review.date.desc()).all()
    elif selected_option == 'oldest-first':
        reviews_original = Review.query.order_by(Review.date.asc()).all()
    elif selected_option == 'highest-rated':
        reviews_original = Review.query.order_by(Review.rating.desc()).all()
    elif selected_option == 'lowest-rated':
        reviews_original = Review.query.order_by(Review.rating.asc()).all()
    elif selected_option == 'most-liked':
        reviews_original = Review.query.order_by(Review.likes.desc()).all()
    reviews=[]
    for entry in reviews_original:
        review={}
        review['id']=entry.id
        review['date']=entry.date.strftime("%H:%M %d/%m/%y")
        review['cheese']=Cheese.query.filter_by(id=entry.cheese_id).first().name
        review['user']=User.query.filter_by(id=entry.user_id).first().username
        review['brand']=entry.brand
        review['rating']=entry.rating
        review['review']=entry.review
        review['likes']=entry.likes
        reviews.append(review)
    return render_template('all_ratings.html', reviews=reviews, review_filter_form=review_filter_form)

@ratings.route('/user_profile')
@login_required
def user_profile():
    reviews_original = Review.query.filter_by(user_id=current_user.id).all()
    reviews = []
    for entry in reviews_original:
        review = {}
        review['id']=entry.id
        review['date'] = entry.date.strftime("%H:%M %d/%m/%y")
        review['cheese'] = Cheese.query.filter_by(id=entry.cheese_id).first().name
        review['brand'] = entry.brand
        review['rating'] = entry.rating
        review['review'] = entry.review
        review['likes'] = entry.likes
        reviews.append(review)
    return render_template('user_profile.html',  reviews=reviews)

@ratings.route('/liked_ratings')
@login_required
def liked_ratings():
    reviews_original = current_user.liked
    reviews = []
    for entry in reviews_original:
        review = {}
        review['id']=entry.id
        review['date'] = entry.date.strftime("%H:%M %d/%m/%y")
        review['user'] = User.query.filter_by(id=entry.user_id).first().username
        review['cheese'] = Cheese.query.filter_by(id=entry.cheese_id).first().name
        review['brand'] = entry.brand
        review['rating'] = entry.rating
        review['review'] = entry.review
        review['likes'] = entry.likes
        reviews.append(review)
    return render_template('liked_ratings.html', reviews=reviews)

@ratings.route('/user_ratings/<username>')
@login_required
def user_ratings(username):
    if username == current_user.username:
        return redirect(url_for('ratings.user_profile'))
    else:
        user=User.query.filter_by(username=username).first()
        reviews_original = Review.query.filter_by(user_id=user.id).all()
        reviews = []
        for entry in reviews_original:
            review = {}
            review['id']=entry.id
            review['date'] = entry.date.strftime("%H:%M %d/%m/%y")
            review['cheese'] = Cheese.query.filter_by(id=entry.cheese_id).first().name
            review['brand'] = entry.brand
            review['rating'] = entry.rating
            review['review'] = entry.review
            review['likes'] = entry.likes
            reviews.append(review)
        return render_template('user_ratings.html', username=username, reviews=reviews)

@ratings.route('/new_rating')
@login_required
def new_rating():
    form=ReviewForm()
    selected_rating=0
    return render_template('new_rating.html', form=form, selected_rating=selected_rating)

@ratings.route('/new_rating', methods=['POST'])
@login_required
def new_rating_post():
    form=ReviewForm()
    try:
        cheese=form.cheese.data
        brand=form.brand.data
        rating=form.rating.data
        review=form.review.data
        cheese_to_review=Cheese.query.filter_by(name=cheese).first()
        new_review=Review(date=datetime.now(), cheese_id=cheese_to_review.id, user_id=current_user.id, brand=brand, rating=rating, review=review, likes=0)
        db.session.add(new_review)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('ratings.all_ratings'))

@ratings.route('/edit_rating_handler', methods=['GET', 'POST'])
@login_required
def edit_rating_handler():
    if request.method=='GET':
        id=request.args.get('id')
        return redirect(url_for('ratings.edit_rating', id=id))
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
        return redirect(url_for('ratings.user_profile'))

@ratings.route('/edit_rating', methods=['GET'])
@login_required
def edit_rating():
    id=request.args.get('id')
    review_to_edit=Review.query.filter_by(id=id).first()
    form=ReviewForm()
    form.cheese.default=Cheese.query.filter_by(id=review_to_edit.cheese_id).first().name
    form.brand.default=review_to_edit.brand
    selected_rating=review_to_edit.rating
    form.process()
    return render_template('edit_rating.html', form=form, id=id, selected_rating=selected_rating)

@ratings.route('/like_rating', methods=['POST'])
@login_required
def like_rating():
    review_id=request.args.get('id')
    user_id=current_user.id
    review=Review.query.get(review_id)
    user=User.query.get(user_id)
    if review and user:
        if review in user.liked:
            user.liked.remove(review)
            review.likes-=1
        else:
            user.liked.append(review)
            review.likes+=1
        db.session.commit()
        return jsonify({'likes': review.likes})
    return jsonify({'error': 'Review not found'}), 404

@ratings.route('/check_like', methods=['GET']) 
@login_required
def check_like():
    review_id=request.args.get('id')
    user_id=current_user.id
    review=Review.query.get(review_id)
    user=User.query.get(user_id)
    if review and user:
        if review in user.liked:
            return jsonify({'liked': True})
        else:
            return jsonify({'liked': False})
    return jsonify({'error': 'Review not found'}), 404


# delete rating handler
@ratings.route('/delete_rating', methods=['GET', 'POST'])
@login_required
def delete_rating():
    # get id of record to delete and delete from database
    try:
        id = request.args.get('id')
        review_to_delete = Review.query.filter_by(id=id).first()
        db.session.delete(review_to_delete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    # redirect to income page
    return redirect(url_for('ratings.user_profile'))
