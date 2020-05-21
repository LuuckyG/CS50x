from webapp.main.helpers import apology

from flask import Blueprint, render_template
from flask_login import login_required


transactions = Blueprint('transactions', __name__)


@transactions.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return render_template("buy.html", title='Buy')


@transactions.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return render_template("history.html", title='History')


@transactions.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return render_template("sell.html", title='Sell')