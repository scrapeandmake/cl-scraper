from flask import Flask, render_template
from flask.ext.wtf import CsrfProtect

from .extensions import (
    db,
    migrate,
    debug_toolbar,
    bcrypt,
    login_manager,
    config
)

from . import models
from .views.users import users
from .views import api

SQLALCHEMY_DATABASE_URI = "postgres://localhost/cl_scraper"
DEBUG = True
SECRET_KEY = 'development-key'
DEBUG_TB_INTERCEPT_REDIRECTS = False

def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.register_blueprint(users)
    # app.register_blueprint(api, url_prefix="/api/v1")

    config.init_app(app)
    db.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "users.login"

    return app
