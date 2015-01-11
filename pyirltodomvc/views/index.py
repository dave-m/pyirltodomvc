import os
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

@view_config(route_name='home')
def index(request):
    """Index page, redirect to our client side app.
    Ideally our web server would do this
    """
    return HTTPFound(location='/static/index.html')

