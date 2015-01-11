"""Return all of our Todo's"""

from cornice.resource import resource, view
from cornice.util import json_error

# SQLAlchemy
from pyirltodomvc.models import Session, Todo

def format_todo(inst):
    return {'id': inst.id,
            'name': inst.name,
            'isCompleted': inst.is_complete}


@resource(collection_path='/todos', path='/todos/{id}')
class Todos(object):
    """Represent a ``Todo``"""

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        """Get Everything"""
        return {'todos': [format_todo(i) for i in
                          Session.query(Todo).all()]}

    @view(renderer='json')
    def get(self):
        """Get one"""
        id_ = int(self.request.matchdict['id'])
        inst = Session.query(Todo).get(id_)
        if not inst:
            request.matchdict = None
            return HTTPNotFound()
        return format_todo(inst)

    def collection_post(self):
        """Create a new Todo"""
        if len(self.request.errors) > 0:
            return json_error(self.request.errors)
        return {}



