# -*- coding: utf-8 -*-

import os
import unittest

from inplace import app, db
from inplace.models import User, Place, register_user, authenticate_user

app.config.from_object('inplace.config.TestingConfig')

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def test_register(self):
    #     rv = self.app.post('/register', data=dict(login="ivan",
    #                                               email="ivan@example.com",
    #                                               name=u"Иван Петров",
    #                                               password="qwerty",
    #                                               confirm="qwerty"))

    #     self.assertEqual(rv.status_code, 302)

    # def test_place_add_success(self):
    #     rv = self.app.post('/place/add', data = dict(name = "Test name",
    #     description = "Test description"), follow_redirects = True)

    #     self.assertEqual(rv.status_code, 302)

    def test_user_login_success(self):
        u = User("ivan", "ivan@example.com", u"Иван Петров", "qwerty")
        db.session.add(u)
        db.session.commit()

        rv = self.app.post('/login', data = dict(login = u.login, password = u.password))

        self.assertEqual(rv.status_code, 302)

    def test_user_login_fail(self):
        rv = self.app.post('/login', data = dict(login = "login", password = "password"))

        self.assertEqual(rv.status_code, 200)

    def test_user_open_fail(self):
        rv = self.app.get('/user')

        self.assertEqual(rv.status_code, 302)

    def test_user_update_success(self):
        u = User("ivan", "ivan@example.com", u"Иван Петров", "qwerty")
        db.session.add(u)
        db.session.commit()
      
        rv = self.app.get('/user/update/{0}'.format(u.id))

        self.assertEqual(rv.status_code, 200)

    def test_user_update_fail(self):
        rv = self.app.get('/user/update/1')

        self.assertEqual(rv.status_code, 404)

    def test_place_open_success(self):
        p = Place("Cafe Kivach", "Desc Kivach")
        db.session.add(p)
        db.session.commit()

        rv = self.app.get('/place/1')

        self.assertEqual(rv.status_code, 200)

    def test_place_open_fail(self):
        rv = self.app.get('/place/1')

        self.assertEqual(rv.status_code, 404)

suite = unittest.TestLoader().loadTestsFromTestCase(RegistrationTestCase)
        
if __name__ == '__main__':
    unittest.main()

        
