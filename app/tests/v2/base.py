import unittest

from ...v2.db import test_db


class TestDb(unittest.TestCase):

    def setUp(self):
        from app import create_app
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            self.db = test_db()

    def test_entry(self):
        res = self.client.get("/")
        self.assertEqual(200, res.status_code)

if __name__ == "__main__":
    unittest.main()
