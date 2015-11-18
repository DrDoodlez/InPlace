# -*- coding: utf-8 -*-

import os
import unittest

from boxes import app, db
from boxes.models import User, register_user, authenticate_user

app.config.from_object('boxes.config.TestingConfig')

class UserTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        register_user("ivan", "ivan@example.com", u"Иван Петров", "qwerty")
        u = User.query.filter_by(login="ivan").first()

        self.assertEqual(u.email, "ivan@example.com")

    def test_register_nonunique_login(self):
        u = User("ivan", "ivan@example.com", u"Иван Петров", "qwerty")
        db.session.add(u)
        db.session.commit()
        
        self.assertRaises(Exception,
                          register_user,
                          "ivan", "john@example.com",
                          u"Иван Сидоров", "password")

    def test_register_nonunique_email(self):
        u = User("ivan", "ivan@example.com", u"Иван Петров", "qwerty")
        db.session.add(u)
        db.session.commit()

        self.assertRaises(Exception,
                          register_user,
                          "john", "ivan@example.com",
                          u"Иван Сидоров", "password")
        
    def test_authenticate(self):
        u = User("ivan", "ivan@example.com", u"Иван Петров", "qwerty")
        db.session.add(u)
        db.session.commit()
        
        au = authenticate_user("ivan", "qwerty")

        self.assertEqual(u.id, au.id)

    def test_authenticate_failure(self):
        u = User("ivan", "ivan@example.com", u"Иван Петров", "qwerty")
        db.session.add(u)
        db.session.commit()
        
        au = authenticate_user("ivan", "password")

        self.assertIsNone(au)

suite = unittest.TestLoader().loadTestsFromTestCase(UserTestCase)
        
if __name__ == '__main__':
    unittest.main()
