from webapp import db
from webapp.main.helpers import lookup
from webapp.users.models import User
from webapp.transactions.models import Share, Transaction
from webapp.transactions.forms import BuyForm, SellForm

import os
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
            db.session.commit()

        else:
            share.num_shares += form.shares.data
            share.total_value += form.shares.data * stock['price']      

        buy_transaction = Transaction(
                            user_id=current_user.id,
                            share_id=share.id,
                            symbol=stock['symbol'],
                            is_buy=True,
                            price_per_share=stock['price'],
                            num_shares=form.shares.data,
                            dollar_amount=form.shares.data * stock['price'])
        
        db.session.add(buy_transaction)
        
        current_user.last_buy = datetime.utcnow()
        current_user.num_buys += 1
        current_user.cash -= form.shares.data * stock['price']
        current_user.portfolio_value += form.shares.data * stock['price']

        db.session.commit()

        flash(f'Bought {form.shares.data} share(s) of {form.symbol.data}!', 'success')
        return redirect(url_for('main.index'))

    elif request.method == 'GET':
        form.symbol.data = request.args.get('symbol')
        return render_template("buy.html", title='Buy', form=form)

    return render_template("buy.html", title='Buy', form=form)


@transactions.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    form = SellForm()
    form.symbol.choices = [(g.id, g.symbol) for g in Share.query.order_by('symbol').filter_by(user_id=current_user.id).all()]

    if form.validate_on_submit():
        share = db.session.query(Share).get_or_404(form.symbol.data)
        stock = lookup(share.symbol)

        share.num_shares -= form.shares.data
        share.total_value = share.num_shares * stock['price']
        
        bought_moment = db.session.query(Transaction).\
                            filter(Transaction.share_id==share.id).\
                            filter(Transaction.is_buy==True).first()

        sell_transaction = Transaction(
                            user_id=current_user.id,
                            share_id=share.id,
                            symbol=stock['symbol'],
                            is_buy=False,
                            price_per_share=stock['price'],
                            num_shares=form.shares.data,
                            dollar_amount=form.shares.data * stock['price'])
        
        db.session.add(sell_transaction)
        
        if bought_moment.price_per_share < stock['price']:
            current_user.num_positive_sales += 1
        elif bought_moment.price_per_share == stock['price']:
            current_user.num_equal_sales += 1
        else:
            current_user.num_negative_sales += 1
        
        current_user.last_sale = datetime.utcnow()
        current_user.num_sales += 1
        current_user.cash += form.shares.data * stock['price']
        current_user.portfolio_value -= form.shares.data * stock['price']

        db.session.commit()

        flash(f'Sold {form.shares.data} share(s) of {share.symbol}!', 'success')
        return redirect(url_for('main.index'))

    return render_template("sell.html", title='Sell', form=form)


@transactions.route("/history")
@transactions.route("/history/page/<int:page>")
@login_required
def history(page=1):
    """Show history of transactions"""
    transactions = Transaction.query.order_by(Transaction.date.desc()).\
        filter_by(user_id=current_user.id).\
        paginate(page=page, per_page=int(os.environ.get('ROWS_PER_TABLE')))
    return render_template("history.html", title='History', user=current_user, transactions=transactions)


@transactions.route("/buy/instant", methods=["GET", "POST"])
@login_required
def instant_buy():
    """Buy stocks instantly via a modal"""
    if request.form.get('buy-symbol') == "" or request.form.get('buy-shares') == "":
        flash(f"Please fill in all the fields.", "info")
        return redirect(url_for("main.index"))

    symbol = request.form.get('buy-symbol')
    shares = float(request.form.get('buy-shares'))
    
    stock = lookup(symbol)
    if stock and stock['price'] * shares > current_user.cash:
        flash(f"You can't buy {shares} share(s) of {symbol}!", "danger")
        return redirect(url_for("main.index"))
    else:
        share = db.session.query(Share).filter(Share.user_id==current_user.id).filter(Share.symbol==stock['symbol']).first()
        share.num_shares += shares
        share.total_value += shares * stock['price']      

        buy_transaction = Transaction(
                            user_id=current_user.id,
                            share_id=share.id,
                            symbol=stock['symbol'],
                            is_buy=True,
                            price_per_share=stock['price'],
                            num_shares=shares,
                            dollar_amount=shares * stock['price'])
        
        db.session.add(buy_transaction)
        
        current_user.last_buy = datetime.utcnow()
        current_user.num_buys += 1
        current_user.cash -= shares * stock['price']
        current_user.portfolio_value += shares * stock['price']

        db.session.commit()
        
        flash(f'Bought {shares} share(s) of {symbol}!', 'success')
        return redirect(url_for('main.index'))


@transactions.route("/sell/instant", methods=["GET", "POST"])
@login_required
def instant_sell():
    """Sell stocks instantly via a modal"""
    if request.form.get('sell-symbol') == "" or request.form.get('sell-shares') == "":
        flash(f"Please fill in all the fields.", "info")
        return redirect(url_for("main.index"))

    symbol = request.form.get('sell-symbol')
    shares = float(request.form.get('sell-shares'))
    
    stock = lookup(symbol)
    if stock:
        share = db.session.query(Share).filter(Share.user_id==current_user.id).filter(Share.symbol==stock['symbol']).first()
        
        if shares > share.num_shares:
            flash(f"You can't sell {shares} share(s) of {symbol}!", "danger")
            return redirect(url_for("main.index"))
        else:
            share.num_shares -= shares
            share.total_value = share.num_shares * stock['price']      

            bought_moment = db.session.query(Transaction).\
                            filter(Transaction.share_id==share.id).\
                            filter(Transaction.is_buy==True).first()     

            sell_transaction = Transaction(
                                user_id=current_user.id,
                                share_id=share.id,
                                symbol=stock['symbol'],
                                is_buy=False,
                                price_per_share=stock['price'],
                                num_shares=shares,
                                dollar_amount=shares * stock['price'])
            
            db.session.add(sell_transaction)

            if bought_moment.price_per_share < stock['price']:
                current_user.num_positive_sales += 1
            elif bought_moment.price_per_share == stock['price']:
                current_user.num_equal_sales += 1
            else:
                current_user.num_negative_sales += 1
            
            current_user.last_sale = datetime.utcnow()
            current_user.num_sales += 1
            current_user.cash += shares * stock['price']
            current_user.portfolio_value -= shares * stock['price']

            db.session.commit()
            
            flash(f'Sold {shares} share(s) of {symbol}!', 'success')
            return redirect(url_for('main.index'))
    else:
        flash(f"Something went wrong...", "danger")
        return redirect(url_for("main.index"))