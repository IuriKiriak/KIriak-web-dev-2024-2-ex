from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user, logout_user, login_manager

from app import app, db
from .models import User
from query import queries

@app.route('/')
def index():
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            query = queries["SELECT_BOT_INFO_FOR_CARD"]
            cursor.execute(query)
            cards = cursor.fetchall()
            print(cards)
    except:
        db.connect().rollback()
        print("ошибка в полечении информации о всех ботах")
    return render_template('index.html', cards=cards)

@app.route('/show_card/<int:card_id>')
def show_card(card_id):
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            query = queries["SELECT_BOT_INFO_FOR_SHOW"]
            cursor.execute(query, (card_id,))
            bot_info = cursor.fetchone()
            print(bot_info)
    except:
        db.connect().rollback()
        print("ошибка в полечении информации о Боте")
    return render_template("show_card.html", bot=bot_info)



