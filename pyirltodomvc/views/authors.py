"""Return all of our Author's"""

from cornice.resource import resource, view
from cornice.util import json_error

# SQLAlchemy
from pyirltodomvc.models import Session, Author
# Colander
from colander import MappingSchema, SchemaNode, String, Bool


@resource(collection_path='/authors', path='/authors/{id}')
class AuthorsResource(object):
    """Represent a ``Author``"""

    def __init__(self, request):
        self.request = request

    @view(renderer='json_sqla')
    def collection_get(self):
        """Get Everything"""
        return Session.query(Author).all()

    @view(renderer='json_sqla')
    def get(self):
        """Get one"""
        id_ = int(self.request.matchdict['id'])
        inst = Session.query(Author).get(id_)
        if not inst:
            request.matchdict = None
            return HTTPNotFound()
        return inst

