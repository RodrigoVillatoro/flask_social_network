import re
import unittest

from flask import url_for

from app import db, create_app
from app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(b'Stranger' in response.data)

    def test_register_and_login(self):
        # Register account
        response = self.client.post(url_for('auth.register'), data={
            'email': 'name@example.com',
            'username': 'name',
            'password': 'cat',
            'password2': 'cat',
        })
        self.assertTrue(response.status_code == 302)

        # Now login
        response = self.client.post(url_for('auth.login'), data={
            'email': 'name@example.com',
            'password': 'cat',
        }, follow_redirects=True)
        self.assertTrue(re.search(b'Hello,\s+name!', response.data))
        self.assertTrue(
                b'A confirmation email has been sent' in response.data)

        # Send confirmation token
        user = User.query.filter_by(email='name@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                follow_redirects=True)
        self.assertTrue(
            b'You have confirmed your account' in response.data)

        # Log out
        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        self.assertTrue(b'You have been logged out' in response.data)