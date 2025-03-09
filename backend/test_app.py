from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/check-domain', methods=['POST'])
def check_domain():
    data = request.get_json()
    domain = data.get('domain')
    if not domain or ' ' in domain or '.' not in domain:
        return jsonify({'error': 'Invalid domain format'}), 400
    return jsonify({'registered': True})

if __name__ == '__main__':
    app.run(debug=True)

import unittest
from unittest.mock import patch
from app import app

class DomainCheckerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.get')
    def test_valid_domain(self, mock_get):
        mock_response = {
            'status': 'registered',
            'creationDate': '2020-01-01T00:00:00Z'
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.app.post('/check-domain', json={'domain': 'example.com'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('registered', data)
        self.assertTrue(data['registered'])
        self.assertEqual(data['registration_date'], '2020-01-01T00:00:00Z')

    def test_invalid_domain(self):
        response = self.app.post('/check-domain', json={'domain': 'invalid_domain'})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Invalid domain format')

if __name__ == '__main__':
    unittest.main()