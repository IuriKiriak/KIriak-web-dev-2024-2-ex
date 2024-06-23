from flask import render_template, request, redirect, url_for, flash, session, Blueprint

from app import app, db
from query import queries

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/delete_bot/<int:bot_id>', methods=['GET', 'POST'])
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
