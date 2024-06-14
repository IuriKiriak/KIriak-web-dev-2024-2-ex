from flask import Flask, session
from flask_login import LoginManager
from .models import User

app = Flask(__name__)

app.config.from_pyfile('../config.py')

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'index'
login_manager.login_message = 'Доступ к данной странице есть только у авторизованных пользователей'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


from .views import *