# pylint: disable=invalid-name, global-statement, no-member
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine_from_config, inspect

from zope.sqlalchemy import ZopeTransactionExtension
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    # py3k
    from configparser import SafeConfigParser

engine = None

def setup(config):
    """Setup the application given a config dictionary."""

    global engine
    engine = engine_from_config(config, "sqlalchemy.")
    Session.configure(bind=engine)
    return engine

def setup_from_file(fname):
    """Setup the SQLAlchemy configuration from a config file

    """
    config = SafeConfigParser()
    config.read(fname)

    settings = dict(config.items('app:main'))
    setup(settings)

def commit_on_success(func, *arg, **kw):
    """Decorate any function to commit the session on success, rollback in
    the case of error."""

    try:
        result = func(*arg, **kw)
        Session.commit()
    except:
        Session.rollback()
        raise
    else:
        return result

# bind the Session to the current request
Session = scoped_session(sessionmaker())

class Base(object):
    """SQLAlchemy Base class, all common functionality located here

    """


Base = declarative_base(cls=Base)

# establish a constraint naming convention.
# see http://docs.sqlalchemy.org/en/latest/core/constraints.html#configuring-constraint-naming-conventions
#
Base.metadata.naming_convention = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ix": "ix_%(table_name)s_%(column_0_name)s"
}


