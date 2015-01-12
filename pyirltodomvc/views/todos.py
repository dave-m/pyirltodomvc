"""Return all of our Todo's"""

from cornice.resource import resource, view
from cornice.util import json_error

# SQLAlchemy
from pyirltodomvc.models import Session, Todo
# Colander
from colander import MappingSchema, SchemaNode, String, Bool

class TodoSchema(MappingSchema):
    title = SchemaNode(String(), location='body', type=str)
    isCompleted = SchemaNode(Bool(), location='body', type=str)

class TodoEnvelope(MappingSchema):
    todo = TodoSchema()

def format_todo(inst):
    return {'id': inst.id,
            'title': inst.name,
            'isCompleted': inst.is_complete}


@resource(collection_path='/todos', path='/todos/{id}')
class Todos(object):
    """Represent a ``Todo``"""

    def __init__(self, request):
        self.request = request

    @view(renderer='json')
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

    @view(schema=TodoEnvelope)
    def collection_post(self):
        """Create a new Todo.
        Collander provides us schema format validation.
        **It does not check the data contents, we will 
        have to do this in another library
        """
        if len(self.request.errors) > 0:
            return json_error(self.request.errors)

        post_data = self.request.json_body['todo']  # Form validation here
        inst = Todo(name=post_data['title'],
                    is_complete=post_data['isCompleted'])
        Session.add(inst)
        Session.commit()
        return {'todo': format_todo(inst)}

    @view(schema=TodoEnvelope)
    def put(self):
        """Update an instance"""
        id_ = int(self.request.matchdict['id'])
        inst = Session.query(Todo).get(id_)
        if not inst:
            request.matchdict = None
            return HTTPNotFound()

        inst.name = self.request.json_body['todo']['title']
        inst.is_complete = self.request.json_body['todo']['isCompleted']

        Session.commit()
        return format_todo(inst)

    @view(renderer='json')
    def delete(self):
        """Remove the instance"""
        id_ = int(self.request.matchdict['id'])
        inst = Session.query(Todo).get(id_)
        if not inst:
            request.matchdict = None
            return HTTPNotFound()

        Session.delete(inst)
        Session.commit()
        return {'deleted': True}

