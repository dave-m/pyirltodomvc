from tests.helpers import TestBase
from pyirltodomvc.models import Todo

class TestTodos(TestBase):


    def setUp(self):
        """Test setup"""
        super(TestTodos, self).setUp()
        self.db_session.query(Todo).delete()
        self.db_session.commit()

        self.db_session.add(Todo(id=1,
                                 name='Test Todo',
                                 is_complete=False))
        self.db_session.commit()


    def test_get(self):
        """Test a simple GET"""
        resp = self.app.get('/todos')
        expected = {'todos': [
            {'id': 1, 'name': 'Test Todo', 'isCompleted': False}
        ]}
        self.assertEqual(resp.json, expected)
