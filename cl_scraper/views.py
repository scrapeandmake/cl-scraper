from flask import render_template, flash, redirect, request, url_for
from flask.ext.login import login_user, logout_user
from flask.ext.login import login_required, current_user

from .app import app, db
from .forms import LoginForm, RegistrationForm
from .models import Item, Image, User
import random


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form,
                  field).label.text, error), category)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    user = current_user.name.capitalize()
    return render_template("dashboard.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("That email or password is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("A user with that email address already exists.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You have been registered and logged in.")
            return redirect(url_for("dashboard"))
    else:
        flash_errors(form)

    return render_template("register.html", form=form)
