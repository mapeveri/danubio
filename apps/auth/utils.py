from flask_admin.contrib.sqla import ModelView
import flask_login as login
from werkzeug.security import check_password_hash

from app import db
from apps.auth import models


class Auth(object):
    """
    Authentication utils.
    """
    def validate_login(self, check_user=True, user_object=None, passw=None):
        """
        Validate login form fields.

        - **parameters**:
            :param check_user: Check if is a user model.
            :param user_object: User object model.
            :param passw: Password value.
        """
        # Check if get user model
        if not check_user:
            user = user_object
        else:
            user = self.get_user()

        # Check if has parameter passw
        if passw:
            password = passw
        else:
            password = self.password.data

        if user is None:
            if check_user:
                self.username.errors = ('Invalid username', )
            return False

        if not check_password_hash(user.password, password):
            if check_user:
                self.password.errors = ('Invalid password', )
            return False

        if not user.is_active:
            if check_user:
                self.username.errors = ('You are not an user active', )
            return False

        if not user.is_admin:
            if check_user:
                self.username.errors = ('You are not an administrator', )
            return False

        return True

    def get_user(self, username=None):
        """
        Get user object.

        - **parameters**:
            :param username: Username.
        """
        if username:
            return db.session.query(models.User).filter_by(
                username=username
            ).first()
        else:
            return db.session.query(models.User).filter_by(
                username=self.username.data
            ).first()


class ModelViewSecurity(ModelView):
    """
    ModelView admin login required.
    """
    def is_accessible(self):
        return login.current_user.is_authenticated
