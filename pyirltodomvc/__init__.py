from pyramid.config import Configurator
from sqlalchemy import engine_from_config

# SQLAlchemy Config
from pyirltodomvc.models import setup


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('cornice')
    config.include('pyramid_jinja2')

    # SQLAlchemy setup
    setup(settings)

    # Static/HTML route config
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
