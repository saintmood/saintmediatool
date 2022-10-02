import unittest

from fastapi.testclient import TestClient

from application.main import app
from application.settings import settings, test_settings


class BaseTestCase(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.settings = None

    def setUp(self) -> None:
        app.dependency_overrides[settings] = test_settings
        self.client = TestClient(app)
        self.settings = test_settings()

    def tearDown(self) -> None:
        app.dependency_overrides = {}
        self.client = None
        self.settings = None
