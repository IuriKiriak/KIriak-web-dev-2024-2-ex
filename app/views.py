from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from app import app, load_user
from .models import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_data = {}
    if request.method == "POST":
        name = request.form.get("login")
        password = request.form.get("password")
        remember = request.form.get("remember")

        user_data['login'] = name
        user_data['password'] = password
        user_data['password'] = remember

        user = User.users.get(name)
        print(user)
        if user and user['password'] == password:
            user_obj = User(user_id=user['id'], name=user['name'], password=user['password'])
            login_user(user_obj)  # Логиним пользователя

            session['login_error'] = False
            flash("Вы успешно прошли аутентификацию", "success")
            return redirect('/')
        else:
            print("Неправильный логин или пароль")
            flash("Неправильный логин или пароль", "danger")
            session['login_error'] = True

    return render_template('login.html', user=user_data)  # Возвращаем страницу с формой логина


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')
