from wtforms import PasswordField

from app import db, admin
from apps.auth.models import User
from apps.utils import ModelViewSecurity


class UserAdmin(ModelViewSecurity):
    form_columns = (
        'username', 'password', 'email',
        'first_name', 'last_name', 'is_active',
        'is_admin',
    )
    column_list = (
        'username', 'email', 'first_name',
        'last_name', 'is_active', 'date_join',
        'is_admin',
    )

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password = PasswordField()
        return form_class


admin.add_view(UserAdmin(User, db.session))
