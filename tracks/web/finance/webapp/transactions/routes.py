from webapp.main.helpers import apology

from flask import Blueprint
from flask_login import login_required


transactions = Blueprint('transactions', __name__)


@transactions.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@transactions.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")

@transactions.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    return apology("TODO")

@transactions.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")