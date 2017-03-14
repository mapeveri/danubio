from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from app import db
from apps.main import models


class LoginForm(FlaskForm):
    """
    Login form
    """
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    def validate_login(self):
        user = self.get_user()
        if user is None:
            self.username.errors = ('Invalid username', )
            return False

        if not check_password_hash(user.password, self.password.data):
            self.password.errors = ('Invalid password', )
            return False

        if not user.is_active:
            self.username.errors = ('You are not an user active', )
            return False

        if not user.is_admin:
            self.username.errors = ('You are not an administrator', )
            return False

        return True

    def get_user(self):
        return db.session.query(models.User).filter_by(
            username=self.username.data).first()
