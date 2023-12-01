from app import db
from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash


class Cheese(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    
    def __repr__(self):
        return '<Cheese {}>'.format(self.name)

class User(UserMixin, db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    reviews = db.relationship('Review', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cheese_id = db.Column(db.Integer, db.ForeignKey('cheese.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    brand = db.Column(db.String(64))
    review = db.Column(db.String(240))
    rating = db.Column(db.Integer)
    def __repr__(self):
        return '<Review {}>'.format(self.body)
