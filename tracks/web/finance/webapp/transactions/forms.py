from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

from webapp.main.helpers import lookup
from webapp.transactions.models import Share


class BuyForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(), Length(min=2, max=20)])
    shares = FloatField('Shares', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Buy')

    def validate_symbol(self, symbol):
        if not lookup(symbol.data):
            raise ValidationError(f'No share found for {symbol.data}.')

    def validate_shares(self, shares):
        stock = lookup(self.symbol.data)
        if shares.data * stock['price'] > current_user.cash:
            raise ValidationError(f"You can't buy that many share(s) of {self.symbol.data}. You can maximally buy {(current_user.cash / stock['price']):.2f} shares.")


class SellForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(), Length(min=2, max=20)])
    shares = FloatField('Shares', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Sell')

    def validate_symbol(self, symbol):
        share = Share.query.filter_by(user_id=current_user.id).filter_by(symbol=symbol).first()
        if not share:
            raise ValidationError(f"You don't hold any share(s) of {share.symbol}.")

    def validate_shares(self, shares):
        share = Share.query.filter_by(user_id=current_user.id).filter_by(symbol=self.symbol.data).first()
        if share.num_shares > shares.data:
            raise ValidationError(f"You don't hold that many share(s) of {self.symbol.data}. You can maximally sell {share.num_shares} shares.")
