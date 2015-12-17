# -*- coding: utf-8 -*-

import os
import unittest

from InPlace import app, db
from InPlace.models import User, register_user, authenticate_user

app.config.from_object('InPlace.config.TestingConfig')

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        rv = self.app.post('/register', data=dict(login="ivan",
                                                  email="ivan@example.com",
                                                  name=u"Иван Петров",
                                                  password="qwerty",
                                                  confirm="qwerty"))

        self.assertEqual(rv.status_code, 302)

suite = unittest.TestLoader().loadTestsFromTestCase(RegistrationTestCase)
        
if __name__ == '__main__':
    unittest.main()

        
