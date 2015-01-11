# pylint: disable=too-many-ancestors, unused-argument, too-many-public-methods, too-few-public-methods
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import functions
from sqlalchemy.ext.compiler import compiles

class utcnow(functions.FunctionElement):
    """SQLAlchemy Function that represents UTC timestamp

    """
    key = 'utcnow'
    type = DateTime(timezone=True)


class DefaultTableMixin(object):
    """Mixin that represents the core required properties on a table.

    ``id``: Auto-incrementing Integer primarykey
    ``created_datetime``: UTC datetime when this record was created
    ``last_updated_datetime``: UTC datetime when this record was last updated

    """
    id = Column(Integer, primary_key=True, nullable=False)
    created_datetime = Column(DateTime(timezone=True),
                              default=utcnow(), nullable=False)
    last_updated_datetime = Column(DateTime(timezone=True),
                                   default=utcnow(), onupdate=utcnow(),
                                   nullable=False)


def _default_utcnow(element, compiler, **kw):
    """default compilation handler.

    Note that there is no SQL "utcnow()" function; this is a
    "fake" string so that we can produce SQL strings that are dialect-agnostic,
    such as within tests.

    """
    return "utcnow()"


@compiles(utcnow, 'postgresql')
def _pg_utcnow(element, compiler, **kw):
    """Postgresql-specific compilation handler."""

    return "(CURRENT_TIMESTAMP AT TIME ZONE 'utc')::TIMESTAMP WITH TIME ZONE"
