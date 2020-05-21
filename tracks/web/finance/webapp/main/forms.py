from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    symbol = StringField('Symbol', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Find Share')
