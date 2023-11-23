from app import db
class Cheese(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    origin = db.Column(db.String(64), index=True, unique=False)
    brand = db.Column(db.String(64), index=True, unique=False)
    
    def __repr__(self):
        return '<Cheese {}>'.format(self.name)

class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(128))
    reviews = db.relationship('Review', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cheese_id = db.Column(db.Integer, db.ForeignKey('cheese.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price = db.Column(db.Float)
    review = db.Column(db.String(240))
    rating = db.Column(db.Integer)
    def __repr__(self):
        return '<Review {}>'.format(self.body)
