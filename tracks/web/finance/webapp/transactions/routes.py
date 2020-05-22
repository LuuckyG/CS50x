from webapp import db
from webapp.main.helpers import lookup
from webapp.users.models import User
from webapp.transactions.models import Share, BuyTransaction, SellTransaction
from webapp.transactions.forms import BuyForm, SellForm

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user


transactions = Blueprint('transactions', __name__)


@transactions.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    form = BuyForm()

    if form.validate_on_submit():
        stock = lookup(form.symbol.data)        

        share = db.session.query(Share).filter(Share.user_id==current_user.id).filter(Share.symbol==stock['symbol']).first()
        
        if not share:
            share = Share(user_id=current_user.id, 
                          symbol=stock['symbol'],
                          company_name=stock['name'],
                          num_shares=form.shares.data,
                          total_value=form.shares.data * stock['price'])

            db.session.add(share)

        else:
            share.num_shares += form.shares.data
            share.total_value += form.shares.data * stock['price']      

        buy_transaction = BuyTransaction(
                            user_id=current_user.id,
                            share_id=share.id,
                            symbol=stock['symbol'],
                            price_per_share=stock['price'],
                            num_shares=form.shares.data,
                            dollar_amount=form.shares.data * stock['price'],
                            date_bought=datetime.utcnow())
        
        db.session.add(buy_transaction)
        
        current_user.last_trade = datetime.utcnow()
        current_user.num_trades += 1
        current_user.cash -= form.shares.data * stock['price']
        current_user.portfolio_value += form.shares.data * stock['price']

        db.session.commit()

        flash('Bought!', 'success')
        return redirect(url_for('main.index'))

    elif request.method == 'GET':
        form.symbol.data = request.args.get('symbol')
        return render_template("buy.html", title='Buy', form=form)

    return render_template("buy.html", title='Buy', form=form)


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