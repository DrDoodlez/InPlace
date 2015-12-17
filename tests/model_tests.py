# -*- coding: utf-8 -*-

import os
import unittest

from InPlace import app, db
from InPlace.models import User, Place, register_user, authenticate_user, create_place, update_place, delete_place

app.config.from_object('InPlace.config.TestingConfig')

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


class PlaceTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_place(self):
        place = create_place(u"Место", u"Тестовое место")
        
        p = Place.query.filter_by(name=u"Место").first()
        
        self.assertEqual(p.description, u"Тестовое место")

    def test_update_place(self):
        place = Place(u"Место", u"Тестовое место")
        db.session.add(place)
        db.session.commit()

        updated = update_place(place.id, u"Новое место", u"Новое тестовое место")

        self.assertEqual(updated.id, place.id)
        self.assertEqual(updated.name, u"Новое место")
        self.assertEqual(updated.description, u"Новое тестовое место")

    def test_delete_place(self): 
        place = Place(u"Место", u"Тестовое место")
        db.session.add(place)
        db.session.commit()

        delete_place(place.id)

        p = Place.query.get(place.id)
        self.assertEqual(p, None)

#suite = unittest.TestLoader().loadTestsFromTestCase(UserTestCase)
        
if __name__ == '__main__':
    unittest.main()
