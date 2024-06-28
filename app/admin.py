from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from uuid import uuid4
import hashlib
import os

from app import app, db
from query import queries
from .auth import checkRole
from .sanitaizer import sanitaizer_text

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/delete_bot/<int:bot_id>', methods=['GET', 'POST'])
@login_required
@checkRole("delete")
def delete_bot(bot_id):
    print("вы зашли на сраницу удалить бота")
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            query = queries["DELETE_BOT_IN_BOTS_TABLE"]
            cursor.execute(query, (bot_id,))
            db.connect().commit()
            flash('Удаление успешно', 'success')
    except:
        db.connect().rollback()
        print("ошибка при удалении бота")

    return redirect(url_for('index'))


@bp.route('/create_bot', methods=['GET', 'POST'])
@login_required
@checkRole("create")
def create_bot():
    card = {}
    types = []

    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            query = queries["SELECT_TYPES"]
            cursor.execute(query, ())
            types = cursor.fetchall()
    except:
        print("Не удалось получить все типы для ботов")

    if request.method == "POST":
        UserID = current_user.id

        types_form = request.form.getlist('types')

        NameForWhat = request.form.get('NameForWhat')
        NameBot = request.form.get('NameBot')
        ShortDescription = request.form.get('ShortDescription')
        Description = request.form.get('Description')
        Developer = request.form.get('Developer')
        card["NameBot"] = NameBot
        card["ShortDescription"] = ShortDescription
        card["Description"] = Description
        card["Developer"] = Developer

        try:
            file = request.files['CoverImage']
            md5_hash = hashlib.md5(file.read()).hexdigest()
            file.seek(0)

            # Вставка записи о боте в таблицу Bots
            with db.connect().cursor() as cursor:
                Description = sanitaizer_text(Description)
                ShortDescription = sanitaizer_text(ShortDescription)
                query = queries["INSERT_BOT"]
                cursor.execute(query, (NameBot, NameForWhat, Description, ShortDescription, Developer, UserID))
                print("lfflf ",cursor.lastrowid)
                bot_id = cursor.lastrowid

                #добавление пути к файлу и тд если нет такого же md5
                print("мы тут")
                query = "SELECT FileID FROM ImageFiles WHERE MD5Hash = %s"
                print("запрос ")
                cursor.execute(query, (md5_hash,))
                data = cursor.fetchone()
                print(data)
                file_id = None
                if data == None:
                    print("начало")
                    file_name = str(uuid4()) + '_' + secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                    file.save(file_path)

                    mime_type = file.content_type
                    query = queries["INSERT_FILE"]
                    cursor.execute(query, (file_name, file_path, mime_type, md5_hash))

                    file_id = cursor.lastrowid
                else:
                    file_id = data[0]

                print(bot_id, file_id)

                query = queries["INSERT_BOTFILE"]
                cursor.execute(query, (bot_id, file_id))

                print("_" * 100)

                # Добавление записей в BotsType
                for type_name in types_form:
                    query = queries["SELECT_TYPEID"]
                    cursor.execute(query, (type_name,))
                    type_id = cursor.fetchone()[0]

                    query = queries["INSERT_IN_BOTSTYPES"]
                    cursor.execute(query, (bot_id, type_id))


                db.connect().commit()
                flash('Вы добавили бота', 'success')
                return redirect(url_for('index'))

        except Exception as e:
            db.connect().rollback()
            flash(f'Ошибка при добавлении бота: {str(e)}', 'danger')
            return render_template('create_bot.html', types=types, card=card)

    return render_template('create_bot.html', types=types, card=card)



@bp.route('/edit_bot/<bot_id>', methods=['GET', 'POST'])
@login_required
@checkRole("edit")
def edit_bot(bot_id):
    card = {}
    types = []
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            query = queries["SELECT_TYPES"]
            cursor.execute(query, ())
            types = cursor.fetchall()
    except:
        print("не удалось получиь все типы для ботов")

    if request.method == "POST":
        UserID = current_user.id

        types_form = request.form.getlist('types')

        NameForWhat = request.form.get('NameForWhat')
        NameBot = request.form.get('NameBot')
        ShortDescription = request.form.get('ShortDescription')
        Description = request.form.get('Description')
        Developer = request.form.get('Developer')

        card["NameBot"] = NameBot
        card["ShortDescription"] = ShortDescription
        card["Description"] = Description
        card["Developer"] = Developer

        try:
            with db.connect().cursor(named_tuple=True) as cursor:
                #UPDATE users SET NameBot=%s, NameForWhat=%s Description=%s, ShortDescription=%s, Developer=%s where BotID=%s;
                query = queries["UPDATE_Bot"]
                cursor.execute(query,(NameBot, NameForWhat, Description, ShortDescription, Developer, bot_id))
                db.connect().commit()
                flash("вы обновили данные о боте", 'success')
                return redirect(url_for('index'))
        except:
            db.connect().rollback()
            flash("вам не удалось обновить данные о боте", 'danger')

    return  render_template('edit_bot.html', card=card)


@bp.route('/moderation', methods=['GET', 'POST'])
@login_required
@checkRole("moderation")
def moderation_reviews():
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            query = queries["SELECT_ALL_REVIEWS_FOR_MODERATOR"]
            cursor.execute(query, )
            reviews_moder = cursor.fetchall()
            print(reviews_moder)

    except:
        db.connect().rollback()
        flash("вам не удалось обновить данные о боте", 'danger')
    return render_template("moder_reviews.html", reviews_moder=reviews_moder)

@bp.route('/show_reviews/<int:id_review>', methods=['GET', 'POST'])
@login_required
@checkRole("moderation")
def show_reviews(id_review):
    review = {}
    if request.method == "GET":
        try:
            with db.connect().cursor(named_tuple=True) as cursor:
                query = queries["SELECT_ALL_REVIEW_FOR_MODERATOR"]
                cursor.execute(query, (id_review,))
                review = cursor.fetchone()
                print("review", review)

        except:
            db.connect().rollback()
            print("ошибка при отображении запроса")
            flash("вам не удалось обновить данные о боте", 'danger')

    return render_template("show_reviews.html", review=review)


@bp.route('/approval/<int:id_review>', methods=['POST'])
@login_required
@checkRole("moderation")
def approval(id_review):
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            query = queries["UPDATE_STATUS"]
            cursor.execute(query, (2, id_review))
            db.connect().commit()
            flash("вы одобрили отзыв", 'success')

    except:
        db.connect().rollback()
        print("ошибка при обновление статуса бота")
        flash("вам не удалось обновить статус бота", 'danger')

    return moderation_reviews()


@bp.route('/reject/<int:id_review>', methods=['POST'])
@login_required
@checkRole("moderation")
def reject(id_review):
    try:
        with db.connect().cursor(named_tuple=True) as cursor:
            query = queries["UPDATE_STATUS"]
            cursor.execute(query, (3, id_review))
            db.connect().commit()
            flash("вы отклонили отзыв", 'danger')

    except:
        db.connect().rollback()
        print("ошибка при обноваление статуса бота")
        flash("вам не удалось обновить статус бота", 'danger')

    return moderation_reviews()