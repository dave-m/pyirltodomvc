"""UnitTest Helpers

"""
from unittest import TestCase
from pyramid import testing
from webtest import TestApp

from pyirltodomvc.models import Session
from pyirltodomvc.models.meta.base import setup_from_file

class TestBase(TestCase):
    """Test base class to setup & configure our DB"""

    @classmethod
    def setUpClass(cls):
        """Setup our DB access"""
        setup_from_file('tests/testing.ini')

    def setUp(self):
        """Test setup"""
        self.config = testing.setUp()
        self.config.include('cornice')
        self.config.add_route('home', '/')
        self.config.scan('pyirltodomvc')

        self.db_session = Session
        self.app = TestApp(self.config.make_wsgi_app())


