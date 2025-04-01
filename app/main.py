from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.database import db 
from app.models import User, Task
from app.login_manager import login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = '45cf93c4d41348cd9980674ade9a7356'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'danger'

bcrypt = Bcrypt(app)

# Always put Routes at end
from app import routes
