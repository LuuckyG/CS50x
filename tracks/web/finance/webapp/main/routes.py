from webapp import admin, db, bcrypt
from webapp.main.helpers import apology, lookup, usd
from webapp.users.models import User
from webapp.transactions.models import PortFolio, Share, BuyTransaction, SellTransaction

from flask_admin.contrib.sqla import ModelView
from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


main = Blueprint('main', __name__)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(PortFolio, db.session))
admin.add_view(ModelView(Share, db.session))
admin.add_view(ModelView(BuyTransaction, db.session))
admin.add_view(ModelView(SellTransaction, db.session))


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
    return render_template("index.html", title='Home')

@main.errorhandler(Exception)
def handle_exception(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    main.errorhandler(code)(handle_exception)
