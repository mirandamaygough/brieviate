from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_security import Security, SQLAlchemyUserDatastore
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
login_manager = LoginManager(app)  
login_manager.login_view = 'auth.login'

from app import auth, models, cheeses, ratings

#from app import cheeses, models
from .models import User
from .get_cheeses import get_cheeses

# blueprint for auth routes
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

#blueprint for ratings routes
from .ratings import ratings as ratings_blueprint
app.register_blueprint(ratings_blueprint)

# blueprint for cheese routes
from .cheeses import cheeses as cheeses_blueprint
app.register_blueprint(cheeses_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def initial_setup():
    filename = app.static_folder + '/cheeses.txt'
    get_cheeses(filename)