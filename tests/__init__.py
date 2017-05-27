from mongo_spatial import app
import unittest


class MongoSpatialTest(unittest.TestCase):
    """docstring for MongoSpatialTest"""
    app = app

    def assertOK(self, resp):
        self.assertEqual(resp.status_code, 200)
