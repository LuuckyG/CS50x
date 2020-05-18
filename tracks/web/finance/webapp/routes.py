from webapp import app, admin, db, bcrypt
from webapp.models import User, BuyTransaction, SellTransaction
from webapp.forms import LoginForm, RegistrationForm, UpdateAccountForm
from webapp.helpers import apology, lookup, usd

import os
import secrets
from PIL import Image
from flask_admin.contrib.sqla import ModelView
from flask import redirect, render_template, url_for, request, flash, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(BuyTransaction, db.session))
admin.add_view(ModelView(SellTransaction, db.session))


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@app.route("/index")
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("index.html", title='Home')


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Query database for username
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash('Login Unsuccesful. Please check username and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    logout_user()

    # Redirect user to login form
    return redirect(url_for('index'))


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/profile_pics', image_fn)
    
    output_size = (125, 125)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn


@app.route("/account", methods=['GET', 'POST'])
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
        current_user.amount += form.amount.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.amount.data = f'{current_user.amount:.2f}'
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add user to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Redirect user to home page
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for("index"))
    return render_template('register.html', title='Register', form=form)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
