from webapp import db, bcrypt, mail
from webapp.users.models import User
from webapp.users.utils import save_image, send_reset_email
from webapp.users.forms import LoginForm, RegistrationForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm

import os
from datetime import datetime
from flask import Blueprint, redirect, render_template, url_for, request, flash, session, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


users = Blueprint('users', __name__)


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
        
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_password, 
                    starting_cash=form.cash.data,
                    cash=cash)

        db.session.add(user)
        db.session.commit()

        # Redirect user to home page
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for("main.index"))
    return render_template('register.html', title='Register', form=form)


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
        current_user.bio = form.bio.data
        if request.form['cash_option'] == 'deposit':
            current_user.cash += form.cash.data
        else:
            current_user.cash -= form.cash.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.cash.data = 0.0
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """Request password reset"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An reset password email has been send.', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', form=form, title="Reset Password") 


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    """Reset password"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash(f'Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for("users.login"))
    return render_template('reset_token.html', form=form, title="Reset Password")



