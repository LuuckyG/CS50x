from datetime import datetime
from webapp import db


class PortFolio(db.Model):
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='portfolio')
    shares = db.relationship('Share', backref='portfolio', lazy=True)


class Share(db.Model):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    quote = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)


class BuyTransaction(db.Model):
    __tablename__ = 'buy_transaction'
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(100), nullable=False)
    price_per_share = db.Column(db.Float, nullable=False)
    shares_amount = db.Column(db.Float, nullable=False)
    dollar_amount = db.Column(db.Float, nullable=False)
    date_bought = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Bought {self.shares_amount} share(s) of {self.quote} for ${self.dollar_amount}"


class SellTransaction(db.Model):
    __tablename__ = 'sell_transaction'
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(100), nullable=False)
    price_per_share = db.Column(db.Float, nullable=False)
    shares_amount = db.Column(db.Float, nullable=False)
    dollar_amount = db.Column(db.Float, nullable=False)
    date_sold = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Sold {self.shares_amount} share(s) of {self.quote} for ${self.dollar_amount}"
