from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from flask_login import login_required, current_user, login_user, logout_user, LoginManager

from app import app, db
from .models import User
from query import queries

bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_login_manage(app):
    login_manager = LoginManager()

    login_manager.init_app(app)

    login_manager.login_view = 'index'
    login_manager.login_message = 'Доступ к данной странице есть только у авторизованных пользователей'
    login_manager.login_message_category = 'warning'

    login_manager.user_loader(load_user)


def load_user(user_id):
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            query = 'SELECT * FROM Users WHERE UserID=%s'
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(user_data.UserID, user_data.Login)
    except:
        db.connect().rollback()
        print("ошибка при загрузки пользователя")
    return None


@bp.route('/login', methods=['GET', 'POST'])
def login():
    user_data = {}
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        remember = request.form.get("remember")

        user_data['login'] = login
        user_data['password'] = password
        user_data['remember'] = remember
        try:
            with db.connect().cursor(named_tuple=True) as cursor:
                query = 'SELECT * FROM Users WHERE Login=%s AND PasswordHash=SHA2(%s,256)'
                cursor.execute(query, (login, password))
                user_data = cursor.fetchone()
                if user_data:
                    user = User(user_data.UserID, user_data.Login)
                    login_user(user, remember=remember)
                    flash('Вы успешно прошли аутентификацию', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Неверные логин или пароль', 'danger')
        except:
            db.connect().rollback()
            print("ошибка при авторизации")

    return render_template('login.html', user=user_data)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))