from flask import Flask, session
from flask_login import LoginManager
from .models import User, MyDb


app = Flask(__name__)

app.config.from_pyfile('../config.py')

db = MyDb(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'index'
login_manager.login_message = 'Доступ к данной странице есть только у авторизованных пользователей'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    with db.connect().cursor(named_tuple=True) as cursor:
        query = 'SELECT * FROM Users WHERE UserID=%s'
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data.UserID, user_data.Login)
    return None


from .views import *