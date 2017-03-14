from flask_restful import Resource

from app import api
from apps.main import models
from apps.utils import MiximJson


class GetUsers(Resource, MiximJson):
    def get(self):
        users = models.User.query.all()
        return self.to_json(users)


api.add_resource(GetUsers, '/api/getusers')
