import json
import datetime
from sqlalchemy import inspect

from pyirltodomvc.models.meta import Base

def _get_value(value):
    """If the value is a single attribute call ``.json``
    otherwise iterate over each and recurse

    """
    if isinstance(value, (list, tuple)):
        return [_get_value(v) for v in value]
    if isinstance(value, Base):
        return _serialize_instance(value)
    return value

def _serialize_instance(inst):
    mapper = inspect(inst)
    fields = mapper.attrs
    return dict((c.key, _get_value(c.value))
                 for c in fields)

def _serialize_datetime(d):
    if isinstance(d, (datetime.datetime,
                      datetime.date)):
        return d.isoformat()
    return d

def _get_class_name(inst):
    if inst:
        return inst.__class__.__name__.lower()


class SQLAlchemyJSONRenderFactory(object):

    def __init__(self, info):
        """Create our Renderer, currently nothing to do"""

    def __call__(self, value, system):
        """Given ``value`` (a SQLAlchemy instance) return a
        JSONified version of it

        """
        if not value:
            return '{}'

        if not isinstance(value, (list, tuple)):
            # Unify our instance
            value = [value]

        struct = {_get_class_name(value[0]): [_serialize_instance(i) for i in value]}

        return json.dumps(struct, default=_serialize_datetime)

