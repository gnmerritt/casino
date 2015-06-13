from flask import jsonify
from sqlalchemy.orm import class_mapper

def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(model.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(model, c)) for c in columns)


def paged_json(data, pagination=None):
    return jsonify(**{
        "data": data,
        "pagination": pagination,
    })
