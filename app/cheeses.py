# setup of views to navigate through the app
from flask import Flask, render_template, request, Blueprint
from app import app
from app import db
from .forms import ReviewFilterForm
from .models import User, Cheese, Review

cheeses = Blueprint('cheeses', __name__)

# main cheese page
@cheeses.route('/all_cheeses')
def all_cheeses():
    # get all cheeses from database
    cheeses_original=Cheese.query.all()
    cheeses=[]
    # create a dictionary for each cheese with the cheese name, number of ratings and average rating
    for entry in cheeses_original:
        cheese = {}
        cheese['id']=entry.id
        cheese['name']=entry.name
        cheese['ratings']=Review.query.filter_by(cheese_id=entry.id).count()
        #  if there are no ratings, set average rating to 0
        if cheese['ratings'] == 0:
            cheese['average_rating']=0
        #  else calculate the average rating and round to 2 decimal places
        else:
            average_rating = Review.query.filter_by(cheese_id=entry.id).with_entities(db.func.avg(Review.rating)).first()[0]
            cheese['average_rating'] = round(average_rating, 2)
        cheeses.append(cheese)
    return render_template('all_cheeses.html', cheeses=cheeses, title='All Cheeses')

# cheese profile page
@cheeses.route('/cheese_profile/<cheese>')
def cheese_profile(cheese):
    # get the cheese name from the url and convert it to the correct format
    cheese = cheese.replace("-", " ").title()
    # get the cheese object from the database
    cheese_name=Cheese.query.filter_by(name=cheese).first()
    # check which option has been selected in the filter form
    review_filter_form=ReviewFilterForm()
    reviews_original=[]
    if request.method == 'GET' and 'submit' in request.args:
        selected_option = request.args.get('filter_option')
        review_filter_form.filter_option.default = selected_option
        review_filter_form.process()
    else:
        selected_option = 'newest-first'
    # get the reviews for the selected cheese and order them according to the selected option
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
    # create a dictionary for each review with the review details
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
    return render_template('cheese_profile.html', cheese=cheese_name, reviews=reviews, review_filter_form=review_filter_form, title=cheese_name.name)
