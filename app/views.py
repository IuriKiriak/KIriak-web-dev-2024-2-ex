from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    flash('Неправильный логин или пароль', 'danger')
    return redirect(url_for('index'))


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')