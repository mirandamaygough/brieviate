from app import db
from flask_login import UserMixin

# database model for cheeses
class Cheese(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    
    def __repr__(self):
        return '<Cheese {}>'.format(self.name)

# database model for users
class User(UserMixin, db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(25))
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    # user's liked reviews
    liked = db.relationship('Review', secondary='user_likes_review', backref=db.backref('liked', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

# database model for reviews
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # many to many relationship with users and cheeses 
    cheese_id = db.Column(db.Integer, db.ForeignKey('cheese.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, index=True)
    brand = db.Column(db.String(50))
    review = db.Column(db.String(500))
    rating = db.Column(db.Integer)
    likes = db.Column(db.Integer, default=0)
    def __repr__(self):
        return '<Review {}>'.format(self.body)

# database table for likes
user_likes_review = db.Table('user_likes_review',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('review_id', db.Integer, db.ForeignKey('review.id'))
)