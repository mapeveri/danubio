import importlib

from flask import jsonify
from sqlalchemy.orm import class_mapper


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
