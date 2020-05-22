from datetime import datetime
from webapp import db


class Share(db.Model):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symbol = db.Column(db.String(100), nullable=False)
    company_name =  db.Column(db.String(100), nullable=False)
    num_shares = db.Column(db.Integer, nullable=False)
    total_value = db.Column(db.Float, nullable=False, default=0.00)


class BuyTransaction(db.Model):
    __tablename__ = 'buy_transaction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    share_id = db.Column(db.Integer, db.ForeignKey('share.id'), nullable=False)
    symbol = db.Column(db.String(100), nullable=False)
    price_per_share = db.Column(db.Float, nullable=False)
    num_shares = db.Column(db.Float, nullable=False)
    dollar_amount = db.Column(db.Float, nullable=False)
    date_bought = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Bought {self.shares_amount} share(s) of {self.symbol} for ${self.dollar_amount}"


class SellTransaction(db.Model):
    __tablename__ = 'sell_transaction'
    id = db.Column(db.Integer, primary_key=True)
    buy_id = db.Column(db.Integer, db.ForeignKey('buy_transaction.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    share_id = db.Column(db.Integer, db.ForeignKey('share.id'), nullable=False)
    symbol = db.Column(db.String(100), nullable=False)
    price_per_share = db.Column(db.Float, nullable=False)
    num_shares = db.Column(db.Float, nullable=False)
    dollar_amount = db.Column(db.Float, nullable=False)
    date_bought = db.Column(db.DateTime, db.ForeignKey('buy_transaction.date_bought'), nullable=False)
    date_sold = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Sold {self.shares_amount} share(s) of {self.symbol} for ${self.dollar_amount}"
