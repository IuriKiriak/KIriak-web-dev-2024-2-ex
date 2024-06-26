from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from flask_login import current_user, login_required

from app import app, db
from query import queries
from .auth import checkRole

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
        print("не удалось получиь все типы для ботов")

    if request.method == "POST":
        UserID = current_user.id

        types_form = request.form.getlist('types')
        print(types)

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
                query = queries["INSERT_BOT"]
                cursor.execute(query,(NameBot, NameForWhat, Description, ShortDescription, Developer, UserID))
                bot_id = cursor.lastrowid
                # Добавление записей в BotsType
                for type_name in types_form:
                    query = queries["SELECT_TYPEID"]
                    cursor.execute(query, (type_name,))
                    type_id = cursor.fetchone()
                    type_id = type_id[0]

                    query = queries["INSERT_IN_BOTSTYPES"]
                    cursor.execute(query, (bot_id, type_id))

                db.connect().commit()
                flash('Вы добавили бота', 'success')
                return redirect(url_for('index'))
        except:
            db.connect().rollback()
            flash('Ошибка при добавление бота', 'danger')
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
            flash("вам не удалось обновить данные о боте", 'danger')
    return  render_template('edit_bot.html', card=card)