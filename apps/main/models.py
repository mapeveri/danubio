import datetime

from flask import Blueprint
from sqlalchemy import event
from werkzeug.security import generate_password_hash

from app import db, login_manager


class User(db.Model):
    """
    Model User
    """
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    date_join = db.Column(
        db.DateTime, nullable=False,
        default=datetime.datetime.utcnow
    )
    is_active = db.Column(
        db.Boolean, default=True
    )
    is_admin = db.Column(
        db.Boolean, default=False
    )

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        return '<User %r>' % (self.username)


def hash_password(target, value, oldvalue, initiator):
    if value is not None:
        return generate_password_hash(value)

# Setup listener on User attribute password
event.listen(User.password, 'set', hash_password, retval=True)


@login_manager.user_loader
def load_user(id):
    """
    For flask-login get user id
    """
    return User.query.get(int(id))
