from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user, logout_user, login_manager

from app import app, db
from .models import User
from query import queries
from .sanitaizer import sanitaizer_text

PER_PAGE = 9
PER_PAGE_REVIEWS = 1

@app.route('/')
def index():
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            page = request.args.get('page', 1, type=int)
            offset = (page - 1) * PER_PAGE
            query = queries["SELECT_BOT_INFO_FOR_CARD"]
            cursor.execute(query, (PER_PAGE, offset))
            cards = cursor.fetchall()
            print(cards)
            cursor.execute("SELECT COUNT(*) AS total FROM Bots")
            total_records = cursor.fetchone().total
            total_pages = (total_records + PER_PAGE - 1) // PER_PAGE
    except:
        db.connect().rollback()
        print("ошибка в полечении информации о всех ботах")
    return render_template('index.html', cards=cards, page=page, total_pages=total_pages)


@app.route('/show_card/<int:card_id>')
def show_card(card_id):
    review_user = {}
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            page = request.args.get('page', 1, type=int)
            offset = (page - 1) * PER_PAGE_REVIEWS

            query = queries["SELECT_BOT_INFO_FOR_SHOW"]
            cursor.execute(query, (card_id, ))
            bot_info = cursor.fetchone()

            query = queries["SELECT_ALL_REVIEWS"]
            cursor.execute(query, (card_id, PER_PAGE_REVIEWS, offset))
            reviews = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) AS total FROM Reviews WHERE Reviews.BotID = %s and Reviews.StatusID = 2;", (card_id, ))
            total_records = cursor.fetchone().total

            total_pages = (total_records + PER_PAGE_REVIEWS - 1) // PER_PAGE_REVIEWS
            if current_user.is_authenticated == True:
                query = queries["SELECT_USER_REVIEW"]
                cursor.execute(query, (current_user.id, card_id))
                review_user = cursor.fetchone()
                print("review_user: ", review_user)

    except:
        db.connect().rollback()
        print("ошибка в получении информации о Боте")
    return render_template("show_card.html", bot=bot_info, page=page, total_pages=total_pages, reviews=reviews, review_user=review_user)

@app.route('/write_review/<int:bot_id>/<int:user_id>', methods=['GET', 'POST'])
def write_review(bot_id, user_id):
    if request.method == "POST":
        rating = 0
        for star in range(1, 6):
            rating = request.form.get(f"{star}")
            if rating == "on":
                rating = star
                break

        print(f"оценка {rating}")
        user_review = request.form.get("userReview")

        try:
            with db.connect().cursor(named_tuple=True) as cursor:
                query = queries["SELECT_USER_REVIEW"]
                cursor.execute(query, (current_user.id, bot_id))
                review_user = cursor.fetchone()
                if not review_user:
                    user_review = sanitaizer_text(user_review)
                    query = queries["INSERT_REVIEW_USER"]
                    print(bot_id, user_id, rating, user_review)
                    cursor.execute(query, (bot_id, user_id, rating, user_review))
                    db.connect().commit()
                    flash('Вы добавили отзыв', 'success')
                else:
                    flash('вы уже добавили отзыв', 'danger')
                    return show_card(bot_id)
        except:
            db.connect().rollback()
            flash('не получилось добавить отзыв', 'danger')
            print("ошибка в получении информации о Боте")

        print(user_review)
        print(rating)

    return show_card(bot_id)

