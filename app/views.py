from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user, logout_user, login_manager
from app import app#, load_user, db
from .models import User


# def get_roles():
#     with db.connect().cursor(named_tuple=True) as cursor:
#             query = ('SELECT * FROM roles')
#             cursor.execute(query)
#             roles = cursor.fetchall()
#     return roles


@app.route('/')
def index():
    # print(get_roles())
    return render_template('index.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     user_data = {}
#     if request.method == "POST":
#         login = request.form.get("login")
#         password = request.form.get("password")
#         remember = request.form.get("remember")
#
#         user_data['login'] = login
#         user_data['password'] = password
#         user_data['remember'] = remember
#
#         with db.connect().cursor(named_tuple=True) as cursor:
#             query = 'SELECT * FROM Users WHERE Login=%s AND PasswordHash=SHA2(%s,256)'
#             cursor.execute(query, (login, password))
#             user_data = cursor.fetchone()
#             if user_data:
#                 user = User(user_data.UserID, user_data.Login)
#                 login_user(user, remember=remember)
#                 flash('Вы успешно прошли аутентификацию', 'success')
#                 return redirect(url_for('index'))
#             else:
#                 flash('Неверные логин или пароль', 'danger')
#
#     return render_template('login.html', user=user_data)
#
#
#
#
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))


# @app.route('/secret')
# @login_required
# def secret():
#     return render_template('secret.html')

