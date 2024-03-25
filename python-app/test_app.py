import unittest
from flask import url_for
from flask_testing import TestCase

from app import app

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index_page(self):
        response = self.client.get(url_for('index'))
        self.assert200(response)
        self.assertIn(b"Enter Your Name and Age", response.data)

    def test_greet_page(self):
        response = self.client.post(url_for('greet'), data={'name': 'John', 'age': 25}, follow_redirects=True)
        self.assert200(response)
        self.assertIn(b"Hello, John!", response.data)
        self.assertIn(b"You are 25 years old!", response.data)

if __name__ == '__main__':
    unittest.main()