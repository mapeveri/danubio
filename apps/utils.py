import importlib

import flask_login as login
from flask import jsonify, redirect, render_template, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, helpers
from flask_admin.base import AdminIndexView
from sqlalchemy.orm import class_mapper

from apps.main.forms import LoginForm


class ModelViewSecurity(ModelView):
    """
    ModelView admin login required
    """
    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)

        if request.method == 'POST':
            if helpers.validate_form_on_submit(form) and form.validate_login():
                user = form.get_user()
                login.login_user(user)
                return redirect(url_for('admin.index'))

        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class MiximJson(object):
    """
    Mixin for json objects
    """
    def serialize(self, model):
        """
        Transforms a model into a dictionary which can be dumped to JSON.
        """
        columns = [c.key for c in class_mapper(model.__class__).columns]
        return dict((c, getattr(model, c)) for c in columns)

    def to_json(self, query):
        """
        Return in format json query Model
        """
        serialized_labels = [
            self.serialize(label)
            for label in query
        ]

        return jsonify(json_list=serialized_labels)


def include(url):
    """
    Include import dynamic
    """
    try:
        importlib.import_module(url)
    except ImportError:
        pass
