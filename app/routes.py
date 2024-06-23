from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user, logout_user, login_manager

from app import app, db
from .models import User
from query import queries

@app.route('/')
def index():
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            page = request.args.get('page', 1, type=int)
            per_page = 9
            offset = (page - 1) * per_page
            query = queries["SELECT_BOT_INFO_FOR_CARD"]
            cursor.execute(query, (per_page, offset))
            cards = cursor.fetchall()
            print(cards)
            # получение количества ботов для отображения определенного количества страниц
            cursor.execute("SELECT COUNT(*) AS total FROM Bots")
            total_records = cursor.fetchone().total
            total_pages = (total_records + per_page - 1) // per_page
    except:
        db.connect().rollback()
        print("ошибка в полечении информации о всех ботах")
    return render_template('index.html', cards=cards, page=page, total_pages=total_pages)

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
        print("ошибка в получении информации о Боте")
    return render_template("show_card.html", bot=bot_info)


