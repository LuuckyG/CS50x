from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import SelectField, StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from sqlalchemy import table, column, select

from webapp import db
from webapp.main.helpers import lookup
from webapp.users.models import User
from webapp.transactions.models import Share


class BuyForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(), Length(min=2, max=20)])
    shares = FloatField('Shares', validators=[DataRequired(), NumberRange(min=0.001)])
    submit = SubmitField('Buy')

    def validate_symbol(self, symbol):
        if not lookup(symbol.data):
            raise ValidationError(f'No share found for {symbol.data}.')

    def validate_shares(self, shares):
        stock = lookup(self.symbol.data)
        if shares.data * stock['price'] > current_user.cash:
            raise ValidationError(f"You can't buy that many share(s) of {self.symbol.data}. You can maximally buy {(current_user.cash / stock['price']):.2f} shares.")


class SellForm(FlaskForm):
    symbol = SelectField('Symbol', coerce=int)
    shares = FloatField('Shares', validators=[DataRequired(), NumberRange(min=0.001)])
    submit = SubmitField('Sell')

    def validate_shares(self, shares):
        
        share = Share.query.get_or_404(self.symbol.data)

        if  shares.data > share.num_shares:
            raise ValidationError(f"You don't hold that many share(s) of {share.symbol}. You can maximally sell {(share.num_shares):.2f} shares.")
