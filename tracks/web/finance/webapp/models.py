from datetime import datetime
from flask_login import UserMixin
from webapp import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    amount = db.Column(db.Float, default=10000.00)

    def __repr__(self):
        return f"User {self.username} - Balance: ${self.amount}"

class BuyTransactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(100), nullable=False)
    shares_amount = db.Column(db.Float, nullable=False)
    dollar_amount = db.Column(db.Float, nullable=False)
    price_per_share = db.Column(db.Float, nullable=False)
    total_bought = db.Column(db.Float, nullable=False)
    date_bought = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Bought {self.shares_amount} share(s) of {self.quote} for ${self.dollar_amount}"

class SellTransactions(db.Model):
    __tablename__ = 'sell_transactions'
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(100), nullable=False)
    shares_amount = db.Column(db.Float, nullable=False)
    dollar_amount = db.Column(db.Float, nullable=False)
    price_per_share = db.Column(db.Float, nullable=False)
    total_sold = db.Column(db.Float, nullable=False)
    date_sold = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Sold {self.shares_amount} share(s) of {self.quote} for ${self.dollar_amount}"