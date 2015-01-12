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


    def test_get_all(self):
        """Test a simple GET"""
        resp = self.app.get('/todos')
        expected = {'todos': [
            {'id': 1, 'title': 'Test Todo', 'isCompleted': False}
        ]}
        self.assertEqual(resp.json, expected)

    def test_get_one(self):
        """Test getting a single instance"""
        resp = self.app.get('/todos/1')
        expected = {'id': 1,
                    'title': 'Test Todo',
                    'isCompleted': False}
        self.assertEqual(resp.json, expected)


    def test_post(self):
        """Test creating a new Todo"""
        new_todo = {'todo': {'title': 'Test Creating a todo',
                             'isCompleted': True}}
        resp = self.app.post_json('/todos', new_todo)
        got = resp.json['todo']
        got.pop('id')  # Auto incrementing, so can't check

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(got, {'title': 'Test Creating a todo',
                               'isCompleted': True})

    def test_put(self):
        """Test updating an existing Todo"""
        data = {"todo":{"title": "Test Todo Update",
                        "isCompleted": True}}
        resp = self.app.put_json('/todos/1', data)

        self.assertEqual(resp.status_code, 200)

        # Check our updates have been applied
        inst = self.db_session.query(Todo).get(1)
        self.assertEqual(inst.name, data['todo']['title'])
        self.assertEqual(inst.is_complete, data['todo']['isCompleted'])

    def test_delete(self):
        """Test deleting an existing instance"""
        resp = self.app.delete('/todos/1')

        self.assertEqual(resp.status_code, 200)

        # Check it doesn't exist anymore
        inst = self.db_session.query(Todo).get(1)
        self.assertIsNone(inst)
