from flask import request
import flask_login as login
from flask_restful import Resource

from app import api
from apps.auth.utils import Auth


class AuthLogin(Resource, Auth):
    """
    Authentication login api
    """
    def post(self):
        if login.current_user.is_authenticated:
            return {
                'result': 'ok',
                'description': 'Already logged in'
            }

        username = request.form['user']
        password = request.form['password']
        user = self.get_user(username)
        if self.validate_login(False, user, password):
            login.login_user(user)
            return {
                'result': 'ok',
                'description': 'Authentication successful'
            }
        else:
            return {
                'result': 'error',
                'description': 'Error authentication'
            }



class LogOutLogin(Resource, Auth):
    """
    Logout api
    """
    def post(self):
        if login.current_user.is_authenticated:
            login.logout_user()
            return {
                'result': 'ok',
                'description': 'Logout'
            }
        else:
            return {
                'result': 'error',
                'description': 'You are not logged in'
            }


api.add_resource(AuthLogin, '/api/auth')
api.add_resource(LogOutLogin, '/api/logout')
