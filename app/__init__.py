from flask import Flask, session

from .models import User, MyDb

app = Flask(__name__)

app.config.from_pyfile('../config.py')

db = MyDb(app)

from .auth import bp as bp_auth, init_login_manage

init_login_manage(app)

app.register_blueprint(bp_auth, url_prefix='/auth')

from .views import *