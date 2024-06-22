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
            # for card in cards:
            #     try:
            #         type_card = card[2].split(", ")
            #         card[2] = type_card
            #     except:
            #         card = None
    except:
        print("ошибка в полечении информации о всех ботах")
    return render_template('index.html', cards=cards)

