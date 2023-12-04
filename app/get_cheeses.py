from app import db
from .models import Cheese

def get_cheeses(filename):
    with open(filename, 'r') as file:
        cheeses = file.readlines()
        for cheese_name in cheeses:
            # remove extra whitespace
            cheese_name = cheese_name.strip()

            # check if the cheese already exists in the database to avoid duplicates
            existing_cheese = Cheese.query.filter_by(name=cheese_name).first()

            if not existing_cheese:
                cheese = Cheese(name=cheese_name)
                db.session.add(cheese)

        db.session.commit()