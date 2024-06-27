from flask import Flask, session

from .models import User, MyDb

app = Flask(__name__)

app.config.from_pyfile('../config.py')

db = MyDb(app)

from .auth import bp as bp_auth, init_login_manage
from .admin import bp as bp_admin
from .user import bp as bp_user

app.register_blueprint(bp_admin, url_prefix='/admin')

init_login_manage(app)

app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_user, url_prefix='/user')


from .routes import *