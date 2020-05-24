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


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    share_id = db.Column(db.Integer, db.ForeignKey('share.id'), nullable=False)
    symbol = db.Column(db.String(100), nullable=False)
    is_buy = db.Column(db.Boolean, nullable=False)
    price_per_share = db.Column(db.Float, nullable=False)
    num_shares = db.Column(db.Float, nullable=False)
    dollar_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        if self.is_buy:
            return f"Bought {self.num_shares} share(s) of {self.symbol} for ${self.dollar_amount}"
        else:
            return f"Sold {self.num_shares} share(s) of {self.symbol} for ${self.dollar_amount}"
