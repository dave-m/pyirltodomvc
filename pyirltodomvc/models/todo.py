# pylint: disable=too-few-public-methods
from .meta import Base, DefaultTableMixin, utcnow
from sqlalchemy import ForeignKey, Enum, Column, Integer, Unicode, Boolean, Table
from sqlalchemy.orm import relationship

tags_to_todo_association = Table('todo_tags',
                                 Base.metadata,
                                 Column('todo_id', Integer, ForeignKey('todo.id')),
                                 Column('tag_id', Integer, ForeignKey('tag.id')),
                                 # For search we might have a different weight for each Todo
                                 Column('weight', Integer, nullable=True),
                                 )

class Todo(DefaultTableMixin, Base):
    """Represent a Todo record

    """
    __tablename__ = "todo"

    name = Column(Unicode(), nullable=False)
    is_complete = Column(Boolean())

    # Author
    author_id = Column(Integer, ForeignKey('author.id'), nullable=True)
    author = relationship("Author")
                         # FOR DEMO, backref="todos")

    tags = relationship("Tag",
                        secondary=tags_to_todo_association)
                        # FOR DEMO, backref="todos")


class Author(DefaultTableMixin, Base):
    """An author of a Todo item"""
    __tablename__ = "author"

    name = Column(Unicode(), nullable=False)
    email = Column(Unicode(), nullable=True)


class Tag(DefaultTableMixin, Base):
    """A Tag"""
    __tablename__ = "tag"

    name = Column(Unicode())

