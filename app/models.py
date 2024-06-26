from flask_login import UserMixin
from .check_rights import CheckRights
import mysql.connector
from flask import g

MODERATOR_ROLE_ID = 2
ADMIN_ROLE_ID = 1
USER_ROLE_ID = 3

class User(UserMixin):
    def __init__(self, user_id, login, role_id):
        self.id = user_id
        self.login = login
        self.role_id = role_id

    def is_admin(self):
        return ADMIN_ROLE_ID == self.role_id

    def is_moder(self):
        return MODERATOR_ROLE_ID == self.role_id

    def can(self, action, record=None):
        check_rights = CheckRights(record)
        method = getattr(check_rights, action, None)
        if method:
            return method()
        return False

class MyDb:
    def __init__(self, app):
        self.app = app
        self.app.teardown_appcontext(self.close_db)

    def get_config(self):
        return {
            'user': self.app.config['MYSQL_USER'],
            'password': self.app.config['MYSQL_PASSWORD'],
            'host': self.app.config['MYSQL_HOST'],
            'database': self.app.config['MYSQL_DATABASE']
        }

    def connect(self):
        if 'db' not in g:
            g.db = mysql.connector.connect(**self.get_config())
        return g.db

    def close_db(self, e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()