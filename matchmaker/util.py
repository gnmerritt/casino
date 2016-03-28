from flask import jsonify
from sqlalchemy.orm import class_mapper


def serialize(model, extras={}, scrub=[]):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    if not model:
        return None
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    values = dict((c, getattr(model, c)) for c in columns)
    if extras:
        for k, v in extras.items():
            values[k] = v
    for k in scrub:
        del values[k]
    return values


def paged_json(data, pagination=None):
    return jsonify(**{
        "data": data,
        "pagination": pagination,
    })
