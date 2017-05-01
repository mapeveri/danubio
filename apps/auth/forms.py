from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

from apps.auth.utils import Auth


class LoginForm(FlaskForm, Auth):
    """
    Login form.

    - **parameters**:
        :param username: Username.
        :param password: Password login.
    """
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
