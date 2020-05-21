from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

from webapp.main.helpers import lookup


class BuyForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(), Length(min=2, max=20)])
    shares = FloatField('Shares', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Buy')

    def validate_symbol(self, symbol):
        if not lookup(symbol.data):
            raise ValidationError(f'No share found for {symbol.data}.')

    def validate_shares(self, symbol, share):
        if share * share.price > current_user.cash:
            raise ValidationError(f"You can't by that many share(s) of {symbol.data}. You can maximally buy {(current_user.cash / share.price):.2f} shares.")


class SellForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(), Length(min=2, max=20)])
    shares = FloatField('Shares', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Sell')

    def validate_symbol(self, symbol):
        if not lookup(symbol.data):
            raise ValidationError(f"You don't hold any share(s) of {symbol.data}.")

    def validate_shares(self, symbol, share):
        if share > current_user.share.amount:
            raise ValidationError(f"You don't hold that many share(s) of {symbol.data}. You can maximally sell {share.amount} shares.")
