from datetime import datetime
from flask_login import UserMixin
from flask_security import RoleMixin

from webapp import db, login_manager
from webapp.transactions.models import Share, Transaction


# Define access levels
ACCESS = {
    'guest': 0,
    'user': 1,
    'moderator': 2,
    'admin': 3
}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_online = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    starting_cash = db.Column(db.Float, nullable=False)
    cash = db.Column(db.Float, default=0.00)
    portfolio_value = db.Column(db.Float, default=0.00)
    portfolio_size = db.Column(db.Integer, nullable=False, default=0)
    num_buys = db.Column(db.Integer, nullable=False, default=0) 
    num_sales = db.Column(db.Integer, nullable=False, default=0)
    num_equal_sales = db.Column(db.Integer, nullable=False, default=0)
    num_positive_sales = db.Column(db.Integer, nullable=False, default=0)
    num_negative_sales = db.Column(db.Integer, nullable=False, default=0)
    last_buy = db.Column(db.DateTime)
    last_sale = db.Column(db.DateTime)
    status = db.Column(db.Boolean, nullable=False, server_default='1')
    access = db.Column(db.Integer, nullable=False, default=1)
    roles = db.relationship('Role', secondary='user_roles')
    shares = db.relationship('Share', backref='owner', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return f"{self.username}"

    def is_admin(self):
        return self.access == ACCESS['admin']
    
    def allowed(self, access_level):
        return self.access >= access_level


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))
