from .app import db
from .extensions import bcrypt, login_manager
from flask.ext.login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def get_password(self):
        return getattr(self, "_password", None)
        return self._password

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Item(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('image.item_id'),
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    created = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float(Precision=64), nullable=True)
    longitude = db.Column(db.Float(Precision=64), nullable=True)
    updated = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)

    images = db.relationship('Image', backref=db.backref('Item',
                             lazy='dynamic'))

    def __repr__(self):
        return "{}".format(self.name)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer)
    image = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "{}".format(self.image)

import cl_scraper.views
