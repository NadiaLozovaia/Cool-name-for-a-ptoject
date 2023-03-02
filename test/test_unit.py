import unittest

from app.endpoints import hello_world
from app.init_db import company_name_check


class TestEndpoints(unittest.TestCase):

    def test_hello_world(self):
        self.assertDictEqual(hello_world(), {"Hello": "World"})


class TestInitDb(unittest.TestCase):
    def test_name_check(self):
        name_lat, name_second = company_name_check(["asdf", "фывап"])
        self.assertEqual(name_lat, "asdf")
        self.assertEqual(name_second, "фывап")

        name_lat, name_second = company_name_check(["фывап", "asdfg"])
        self.assertEqual(name_lat, "asdfg")
        self.assertEqual(name_second, "фывап")
    
        name_lat, name_second = company_name_check("asdf")
        self.assertEqual(name_lat, "asdf")
        self.assertEqual(name_second, None)