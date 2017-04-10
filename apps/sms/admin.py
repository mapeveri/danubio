from wtforms import PasswordField

from app import db, admin
from apps.sms.models import Message
from apps.auth.utils import ModelViewSecurity


class MessageAdmin(ModelViewSecurity):
    form_columns = (
        'message', 'number', 'created',
        'internal_id', 'user'
    )
    column_list = (
        'message', 'number', 'created',
        'internal_id', 'user'
    )

admin.add_view(MessageAdmin(Message, db.session))
