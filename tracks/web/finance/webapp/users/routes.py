from webapp import db, bcrypt
from webapp.users.models import User
from webapp.users.utils import save_image
from webapp.users.forms import LoginForm, RegistrationForm, UpdateAccountForm
from webapp.transactions.models import BuyTransaction, SellTransaction

import os
from datetime import datetime
from flask import Blueprint, redirect, render_template, url_for, request, flash, session, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


users = Blueprint('users', __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Query database for username
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            # Set status to online
            user.status = 1
            db.session.commit()

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.index"))
        else:
            flash('Login Unsuccesful. Please check username and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@users.route("/logout")
def logout():
    """Log user out"""

    # Update status to offline
    current_user.status = 0
    current_user.last_online = datetime.utcnow()
    db.session.commit()

    # Forget any user_id
    session.clear()
    logout_user()

    # Redirect user to login form
    return redirect(url_for('users.login'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Show user account"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.cash += form.cash.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
       
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        if not form.cash.data:
            cash = 0.00
        else:
            cash = form.cash.data
        
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, cash=cash)

        db.session.add(user)
        db.session.commit()

        # Redirect user to home page
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for("main.index"))
    return render_template('register.html', title='Register', form=form)
