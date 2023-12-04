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

from app import views, models
from .models import User
from .get_cheeses import get_cheeses

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .views import views as views_blueprint
app.register_blueprint(views_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def initial_setup():
    filename = app.static_folder + '/cheeses.txt'
    get_cheeses(filename)