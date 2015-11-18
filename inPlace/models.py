# -*- coding: utf-8 -*-
from inPlace import db
# TODO: добавить корректную модель
accept_colors = ["red", "green", "blue", "yellow", "magenta", "cyan",
                 "black", "white", "brown"]

class ModelError(Exception):
    pass

class DuplicateNameError(ModelError):
    pass

class DuplicateColorError(ModelError):
    pass

class WrongColorError(ModelError):
    pass

class Box(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    color = db.Column(db.Enum(*accept_colors))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return '<Box %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(64), unique = True)
    name = db.Column(db.String(128))
    password = db.Column(db.String(64))
    boxes = db.relationship('Box', backref='user', lazy='dynamic')

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

def create_box(user, name, color):
    box = Box(name, color)

    # Если у пользователя уже есть коробочка с таким именем
    if filter(lambda b: b.name == name, user.boxes):
        raise DuplicateNameError
    
    # Если у пользователя уже есть коробочка с таким цветом
    if filter(lambda b: b.color == color, user.boxes):
        raise DuplicateColorError
    
    user.boxes.append(box)
    db.session.add(user)
    db.session.commit()

    return box
