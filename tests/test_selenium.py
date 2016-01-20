import re
import threading
import time
import unittest

from selenium import webdriver

from app import create_app, db
from app.models import Post, Role, User


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # Start Firefox
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        # Skip the following tests if the browser could not be started
        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            # create database and populate with fake data
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            # add an administrator user
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='name@example.com', username='name',
                         password='cat', role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # Start Flask server in a separate thread
            threading.Thread(target=cls.app.run).start()

            # give the server three seconds to ensure it's up
            time.sleep(3)


    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # Stop the server and browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            # Destroy DB
            db.drop_all()
            db.session.remove()

            # Remove app context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # Navigate to the home page
        self. client.get('http://localhost:5000')
        self.assertTrue(re.search('Hello,\s+Stranger',
                        self.client.page_source))

        # Navigate to the login page
        self.client.find_element_by_link_text('Log In').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)

        # Login
        self.client.find_element_by_name('email').send_keys('name@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+name', self.client.page_source))

        # Navigate to user profile page
        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>name</h1>' in self.client.page_source)
