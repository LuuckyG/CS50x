from webapp import admin, db, bcrypt
from webapp.main.forms import SearchForm
from webapp.main.helpers import lookup
from webapp.users.models import User
from webapp.transactions.models import Share, Transaction

from flask_admin.contrib.sqla import ModelView
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


main = Blueprint('main', __name__)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Share, db.session))
admin.add_view(ModelView(Transaction, db.session))


# Ensure responses aren't cached
@main.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@main.route("/")
@main.route("/index")
@login_required
def index():
    """Show portfolio of stocks"""
    user = User.query.filter_by(username=current_user.username).first()
    shares = Share.query.order_by(Share.total_value.desc()).filter_by(user_id=user.id).all()

    current_portfolio_value = 0.00

    for share in shares:
        current_value = lookup(share.symbol)['price']
        current_total_value = share.num_shares * current_value
        share.total_value = current_total_value
        current_portfolio_value += current_total_value
    
    user.portfolio_value = current_portfolio_value
    db.session.commit()

    return render_template("index.html", title='Portfolio', user=user, shares=shares)


@main.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Search shares based on symbol"""
    form = SearchForm()
    if form.validate_on_submit():
        stock = lookup(form.symbol.data)
        if stock:
            return render_template("quote.html", title='Quote', stock=stock)
        else:
            flash(f'Could not find a stock with symbol {form.symbol.data}', 'danger')
            return redirect(url_for('main.quote'))
    return render_template("quote.html", title='Quote', form=form)
