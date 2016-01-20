import json
import unittest

from base64 import b64encode
from flask import url_for

from app import db, create_app
from app.models import Role, User


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers('email', 'password')
        )
        self.assertTrue(response.status_code == 404)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'not found')

    def test_no_auth(self):
        response = self.client.get(
            url_for('api.get_posts', content_type='application/json'))
        self.assertTrue(response.status_code == 200)

    def test_bad_auth(self):
        # Add user
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='name_two@example.com', password='cat', confirmed=True,
                 role=r)
        db.session.add(u)
        db.session.commit()

        # Authenticate with wrong password
        response = self.client.get(
                url_for('api.get_posts'),
                headers=self.get_api_headers('name_two@example.com', 'dog'))
        self.assertTrue(response.status_code == 401)

    def test_token_auth(self):
        # Add user
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='name@example.com', password='cat', confirmed=True,
                 role=r)
        db.session.add(u)
        db.session.commit()

        # Issue request with bad token
        response = self.client.get(
             url_for('api.get_posts'),
             headers=self.get_api_headers('bad-token', '')
        )
        self.assertTrue(response.status_code == 401)

        # Get a Token
        response = self.client.get(
            url_for('api.get_token'),
            headers=self.get_api_headers('name@example.com', 'cat'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # Issue a request with the token
        response = self.client.get(
         url_for('api.get_posts'),
         headers=self.get_api_headers(token, ''))
        self.assertTrue(response.status_code == 200)

    def test_anonymous(self):
        response = self.client.get(
            url_for('api.get_posts'),
            headers=self.get_api_headers('', ''))
        self.assertTrue(response.status_code == 200)