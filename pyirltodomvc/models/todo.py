# pylint: disable=too-few-public-methods
from .meta import Base, DefaultTableMixin, utcnow
from sqlalchemy import ForeignKey, Enum, Column, Integer, Unicode, Boolean
from sqlalchemy.orm import relationship


class Todo(DefaultTableMixin, Base):
    """Represent a Todo record

    """
    __tablename__ = "todo"

    name = Column(Unicode())
    is_complete = Column(Boolean())
