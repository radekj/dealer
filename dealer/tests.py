import unittest

from pyramid import testing
from collections import deque


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home_view(self):
        from .views import TableView
        from .cards import Cards
        from .config import PLAYERS

        request = testing.DummyRequest()
        view = TableView(request)
        data = view.display_table()

        self.assertIn(
            data['actual_player'],
            [player['name'] for player in PLAYERS.values()]
        )
        self.assertEquals(data['bet'], 10)
        self.assertEquals(data['distribution'], 1)
        self.assertEquals(data['phase'], 'pre-flop')
        self.assertIsInstance(data['players'], deque)
        self.assertEquals(data['pot'], 15)
        self.assertIsInstance(data['table'], Cards)


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from dealer import main
        from webtest import TestApp
        self.testapp = TestApp(main({}))

    def test_home(self):
        resp = self.testapp.get('/', status=200)
        body = resp.body.decode(resp.charset)
        self.assertIn('Distribution', body)
        self.assertIn('Bet', body)
        self.assertIn('Pot', body)