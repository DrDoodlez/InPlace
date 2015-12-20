# -*- coding: utf-8 -*-
from InPlace import app, db
import uuid, os

class ModelError(Exception):
    pass

class DuplicateNameError(ModelError):
    pass

##################################################################################
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

## getter: return user or None
def get_user(user_id):
    return User.query.get(user_id)

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

##################################################################################
###   Place
class Place(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ## Отношения для событий и комментариев
    events = db.relationship('Event', backref='place', lazy='dynamic')
    comments = db.relationship('Comment', backref='place', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

## getter: return place or None
def get_place(place_id):
    return Place.query.get(place_id)

def create_place(name, description):
    place = Place(name, description)

    queryPlace = Place.query.filter_by(name=name, description=description).first()
    
    if not queryPlace:
        db.session.add(place)
        db.session.commit()
        return place

    return None

def update_place(place, name, description):
    # place = get_place(place_id)
    
    # if not place:
    #     return None
    
    place.name = name
    place.description = description
    db.session.commit()
    return place

def delete_place(place):
    # if not get_place(place_id):
    #     False

    Place.query.filter_by(id = place.id).delete()
    db.session.commit()
    return True

# Поиск без подстрок
def find_place(name):
    queryPlace = Place.query.filter_by(name=name)
    return queryPlace

###   User-Place operation
def add_place_to_user(user, place):
    # user = get_user(user_id)
    # place = get_place(place_id)
    
    # if not user or not place:
    #     return False
    
    user.places.append(place)
    db.session.add(user)
    db.session.commit()
    return True

def delete_place_from_user(user, place):
    # user = get_user(user_id)
    # place = get_place(place_id)
    
    # if not user or not place:
    #     return False
    
    user.places.remove(place)
    db.session.add(user)
    db.session.commit()
    return True


##################################################################################
###   Event   - Not Used
class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64), unique = True)
    date = db.Column(db.String(64))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

    def __init__(self, name, description, date):
        self.name = name
        self.description = description
        self.date = date

def get_event(event_id):
    return Event.query.get(event_id)

def create_event(name, description, date):
    event = Event(name, description, date)

    queryPlace = Event.query.filter_by(name=name, description=description).first()
    
    if not queryPlace:
        db.session.add(event)
        db.session.commit()
        return event

    return None

def update_event(event, name, description, date):
    # event = get_event(event_id)
    
    # if not event:
    #     return None
    
    event.name = name
    event.description = description
    event.date = date
    db.session.commit()
    return event

def delete_event(event):
    # if not get_event(event_id):
    #     return False
    
    Event.query.filter_by(id = event.id).delete()
    db.session.commit()
    return True

###   Place-Event operation
def add_event_to_place(place, event):
    # place = get_place(place_id)
    # event = get_event(event_id)
    
    # if not event or not place:
    #     return False    
    
    place.events.append(event)
    db.session.add(place)
    db.session.commit()
    return True

def delete_event_from_place(place, event):
    # place = get_place(place_id)
    # event = get_event(event_id)
    
    # if not event or not place:
    #     return False

    place.events.remove(event)
    db.session.add(place)
    db.session.commit()
    return True

##################################################################################
###   Comment   - Not Used
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(64))
    text = db.Column(db.String(64), unique = True)
    date = db.Column(db.Date)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

    def __init__(self, author, text, date):
        self.author = author
        self.text = text
        self.date = date

def get_comment(comment_id):
    return Comment.query.get(comment_id)

def create_comment(author, text, date):
    comment = Comment(author, text)

    queryComment = Comment.query.filter_by(author=author, text=text).first()
    
    if not queryComment:
        db.session.add(comment)
        db.session.commit()
        return comment

    return None

def update_comment(comment, author, text):
    # comment = get_comment(comment_id)

    # if not comment:
    #     return None
    
    comment.author = author
    comment.text = text
    comment.date = date
    db.session.commit()
    return comment

def delete_comment(comment):
    # if not get_comment(comment_id):
    #     return False
    
    Comment.query.filter_by(id = comment.id).delete()
    db.session.commit()
    return True


###   Place-comment operation
def add_comment_to_place(place, comment):
    # place = Place.query.get(place_id)
    # comment = Comment.query.get(comment_id)

    # if not comment or not place:
    #     return False    

    place.events.append(comment)
    db.session.add(place)
    db.session.commit()
    return True

def delete_comment_from_place(place, comment):
    # place = Place.query.get(place_id)
    # comment = Comment.query.get(comment_id)

    # if not comment or not place:
    #     return False    

    place.events.remove(comment)
    db.session.add(place)
    db.session.comment()
    return True