from .app import db
from .extensions import bcrypt, login_manager
from flask.ext.login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    created = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(255), nullable=True)
    longitude = db.Column(db.String(255), nullable=True)
    updated = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)

    images = db.Column(db.foreign)

    def __init__(self, name, url, created):
        self.name = name
        self.url = url
        self.created = created

    def __repr__(self):
        return "{}".format(self.name)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)

import views
