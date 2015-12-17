# -*- coding: utf-8 -*-
from InPlace import app, db
import uuid, os

class ModelError(Exception):
    pass

class DuplicateNameError(ModelError):
    pass

###   User
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(64), unique = True)
    name = db.Column(db.String(128))
    password = db.Column(db.String(64))
    places = db.relationship('Place', backref='user', lazy='dynamic')

    def __init__(self, login, email, name, password):
        self.login = login
        self.email = email
        self.name = name
        self.password = password

def register_user(login, email, name, password):
    user = User(login, email, name, password)

    db.session.add(user)
    db.session.commit()

    return user
        
def authenticate_user(login, password):
    user = User.query.filter_by(login=login).first()
    if user and user.password == password:
        return user

    return None

def set_user_avatar(user, image_file):
    avatar_filename = uuid.uuid4().hex + ".jpg"
    image_file.save(os.path.join(app.config['AVATARS_FOLDER'],
                                   avatar_filename))
    user.avatar_id = avatar_filename

    # TODO: если записать в БД не удалось - удалить файл аватарки
    db.session.add(user)
    db.session.commit()

###   Place
class Place(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, description):
        self.name = name
        self.description = description

def create_place(name, description):
    place = Place(name, description)

    queryPlace = Place.query.filter_by(name=name, description=description).first()
    
    if not queryPlace:
        db.session.add(place)
        db.session.commit()
        return place

    return None

def update_place(place_id, name, description):
    place = Place.query.filter_by(id = place_id).first()
    place.name = name
    place.description = description
    db.session.commit()
    return place

def delete_place(place_id):
    place = Place.query.filter_by(id = place_id).delete()
    db.session.commit()
    return None


###   User-Place operation
def add_place_to_user(user_id, place_id):
    user = User.query.get(user_id)
    place = Place.query.get(place_id)
    user.places.append(place)
    db.session.add(user)
    db.session.commit()
    return None

def delete_place_from_user(user_id, place_id):
    user = User.query.get(user_id)
    place = Place.query.get(place_id)
    user.places.remove(place)
    db.session.add(user)
    db.session.commit()
    return None