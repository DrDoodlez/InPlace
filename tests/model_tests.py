# -*- coding: utf-8 -*-

import os
import unittest

from inplace import app, db
from inplace.models import User, get_user, authenticate_user, register_user
from inplace.models import Place, get_place, create_place, update_place, delete_place, find_place
from inplace.models import Event, get_event, create_event, update_event, delete_event
from inplace.models import Comment, get_comment, create_comment, update_comment, delete_comment
from inplace.models import add_place_to_user, delete_place_from_user
from inplace.models import add_event_to_place, delete_event_from_place, add_event_to_user, delete_event_from_user
from inplace.models import add_comment_to_place, delete_comment_from_place

app.config.from_object('inplace.config.TestingConfig')

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

    # def test_creat_place_long_name(self):
    #     longname = u"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1"
        
    #     self.assertRaises(Exception,
    #                       create_place,
    #                       longname,
    #                       "Тестовое место")

    def test_update_place(self):
        place = Place(u"Место", u"Тестовое место")
        db.session.add(place)
        db.session.commit()

        updated = update_place(place, u"Новое место", u"Новое тестовое место")

        self.assertEqual(updated.id, place.id)
        self.assertEqual(updated.name, u"Новое место")
        self.assertEqual(updated.description, u"Новое тестовое место")

    def test_delete_place(self): 
        place = Place(u"Место", u"Тестовое место")
        db.session.add(place)
        db.session.commit()

        delete_place(place)

        p = get_place(place.id)
        self.assertEqual(p, None)

    # Тест для поиска просто по имени (без подстрок)
    def test_find_place(self): 
        place = Place(u"Место", u"Тестовое место")
        db.session.add(place)
        db.session.commit()

        place = Place(u"Место", u"Тестовое место2")
        db.session.add(place)
        db.session.commit()

        places = find_place(u"Место")

        self.assertEqual(places[0].description, u"Тестовое место")
        self.assertEqual(places[1].description, u"Тестовое место2")


class EventTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_event(self):
        event = create_event(u"Событие", u"Тестовое событие",u"01-01-15")
        
        e = Event.query.filter_by(name=u"Событие").first()
        
        self.assertEqual(e.description, u"Тестовое событие")

    def test_update_event(self):
        event = Event(u"Событие", u"Тестовое событие",u"01-01-15")
        db.session.add(event)
        db.session.commit()

        updated = update_event(event, u"Новое событие", u"Новое тестовое событие","01-01-15")

        self.assertEqual(updated.id, event.id)
        self.assertEqual(updated.name, u"Новое событие")
        self.assertEqual(updated.description, u"Новое тестовое событие")

    def test_delete_event(self): 
        event = Event(u"Место", u"Тестовое место",u"01-01-15")
        db.session.add(event)
        db.session.commit()

        delete_event(event)

        e = Event.query.get(event.id)
        self.assertEqual(e, None)

#suite = unittest.TestLoader().loadTestsFromTestCase(UserTestCase)
        
if __name__ == '__main__':
    unittest.main()
