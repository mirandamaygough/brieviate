# setup of views to navigate through the app
from flask import Flask, render_template, flash, redirect, request, jsonify, url_for, Blueprint
from flask_login import login_required, current_user
from datetime import datetime
from app import app
from app import db
from .forms import ReviewForm, ReviewFilterForm
from .models import User, Cheese, Review

cheeses = Blueprint('cheeses', __name__)

@cheeses.route('/all_cheeses')
def all_cheeses():
    cheeses_original=Cheese.query.all()
    cheeses=[]
    for entry in cheeses_original:
        cheese = {}
        cheese['id']=entry.id
        cheese['name']=entry.name
        cheese['ratings']=Review.query.filter_by(cheese_id=entry.id).count()
        if cheese['ratings'] == 0:
            cheese['average_rating']=0
        else:
            cheese['average_rating']=Review.query.filter_by(cheese_id=entry.id).with_entities(db.func.avg(Review.rating)).first()[0]
        cheeses.append(cheese)
    return render_template('all_cheeses.html', cheeses=cheeses)

@cheeses.route('/cheese_profile/<cheese>')
def cheese_profile(cheese):
    cheese = cheese.replace("-", " ").title()
    cheese_name=Cheese.query.filter_by(name=cheese).first()
    review_filter_form=ReviewFilterForm()
    reviews_original=[]
    if request.method == 'GET' and 'submit' in request.args:
        selected_option = request.args.get('filter_option')
        review_filter_form.filter_option.default = selected_option
        review_filter_form.process()
    else:
        selected_option = 'newest-first'
    if selected_option == 'newest-first':
        reviews_original = Review.query.order_by(Review.date.desc()).filter_by(cheese_id=cheese_name.id).all()
    elif selected_option == 'oldest-first':
        reviews_original = Review.query.order_by(Review.date.asc()).filter_by(cheese_id=cheese_name.id).all()
    elif selected_option == 'highest-rated':
        reviews_original = Review.query.order_by(Review.rating.desc()).filter_by(cheese_id=cheese_name.id).all()
    elif selected_option == 'lowest-rated':
        reviews_original = Review.query.order_by(Review.rating.asc()).filter_by(cheese_id=cheese_name.id).all()
    elif selected_option == 'most-liked':
        reviews_original = Review.query.order_by(Review.likes.desc()).filter_by(cheese_id=cheese_name.id).all()
    reviews=[]
    for entry in reviews_original:
        review={}
        review['id']=entry.id
        review['date']=entry.date.strftime("%H:%M %d/%m/%y")
        review['user']=User.query.filter_by(id=entry.user_id).first().username
        review['brand']=entry.brand
        review['rating']=entry.rating
        review['review']=entry.review
        review['likes']=entry.likes
        reviews.append(review)
        print(cheese_name.name)
    return render_template('cheese_profile.html', cheese=cheese_name, reviews=reviews, review_filter_form=review_filter_form)
