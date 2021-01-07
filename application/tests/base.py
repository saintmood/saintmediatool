import unittest

from fastapi.testclient import TestClient

from application.main import app


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        self.client = None