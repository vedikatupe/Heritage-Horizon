from flask import Flask, jsonify
import unittest

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_splash_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TITLEPAGE', response.data)

    def test_slide_page(self):
        response = self.client.get('/slide')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SLIDE2', response.data)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FSLOGIN', response.data)

    def test_dashboard_page(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DASHBOARD', response.data)

    def test_universe_quiz(self):
        response = self.client.get('/universe/quiz')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'solarquiz', response.data)

    def test_heritage_wordpuzzle(self):
        response = self.client.get('/heritage/wordpuzzle')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'wordpuzzleH', response.data)

if __name__ == '__main__':
    unittest.main()