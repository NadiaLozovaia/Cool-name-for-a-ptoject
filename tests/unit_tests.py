import unittest

from app.endpoints import hello_world

class TestEndpoints(unittest.TestCase):

    def test_hello_world(self):
        self.assertDictEqual(hello_world(), {"Hello": "World"})