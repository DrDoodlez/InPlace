# -*- coding: utf-8 -*-
from InPlace import app, db
import uuid, os

class ModelError(Exception):
    pass

class DuplicateNameError(ModelError):
    pass


##################################################################################
###   Common methods

def set_image(table, image_file, folder):
    image_filename = uuid.uuid4().hex + ".jpg"

    image_file.save(os.path.join(app.config[folder], image_filename))
    table.avatar_id = image_filename
    # TODO: если записать в БД не удалось - удалить файл аватарки
    db.session.add(table)
    db.session.commit()


def delete_old_image(table, folder):
    removed = os.remove(os.path.join(app.config[folder], table.avatar_id))
    if not removed:
        return None 
    db.session.commit()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg', 'gif', 'JPEG'])	


##################################################################################
###   User
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(25), unique = True)
    email = db.Column(db.String(64), unique = True)
    name = db.Column(db.String(128))
    password = db.Column(db.String(64))
    avatar_id = db.Column(db.String(64))
    places = db.relationship('Place', backref='user', lazy='dynamic')
    events = db.relationship('Event', backref='user', lazy='dynamic')

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


##################################################################################
###   Place
class Place(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ## Аватарка 
    avatar_id = db.Column(db.String(64))
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
    app.logger.debug("In update_place: %s", place.name)
    place.name = name
    place.description = description
    app.logger.debug("In update_place name: %s", name)

    # TODO: обработать ошибки добавления нового пользователя       
    db.session.commit()
    app.logger.debug("In update_place NEW: %s", place.name)	
    return place

def delete_place(place):
    Place.query.filter_by(id = place.id).delete()
    db.session.commit()
    return True

# Поиск без подстрок
def find_place(name):
    queryPlace = Place.query.filter_by(name=name)
    return queryPlace

###   User-Place operation
def add_place_to_user(user, place):
    user.places.append(place)
    db.session.add(user)
    db.session.commit()
    return True

def delete_place_from_user(user, place):
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
    event.name = name
    event.description = description
    event.date = date
    db.session.commit()
    return event

def delete_event(event):
    Event.query.filter_by(id = event.id).delete()
    db.session.commit()
    return True

###   Place-Event operation
def add_event_to_place(place, event):
    place.events.append(event)
    db.session.add(place)
    db.session.commit()
    return True

def add_event_to_user(user, event):
    user.events.append(event)
    db.session.add(user)
    db.session.commit()
    return True

def delete_event_from_place(place, event):
    place.events.remove(event)
    db.session.add(place)
    db.session.commit()
    return True

def delete_event_from_user(user_id, event_id):
    user = User.query.get(user_id)
    event = Event.query.get(event_id)
    user.events.remove(event)
    db.session.add(user)
    db.session.commit()
    return None

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
    comment.author = author
    comment.text = text
    comment.date = date
    db.session.commit()
    return comment

def delete_comment(comment):
    Comment.query.filter_by(id = comment.id).delete()
    db.session.commit()
    return True


###   Place-comment operation
def add_comment_to_place(place, comment):
    place.events.append(comment)
    db.session.add(place)
    db.session.commit()
    return True

def delete_comment_from_place(place, comment):
    place.events.remove(comment)
    db.session.add(place)
    db.session.comment()
    return True

##################################################################################
###   Photo   - Not Used
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(64))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    photo_id = db.Column(db.String(64))

    def __init__(self, description, place_id, photo_id):
        self.description = description
        self.place_id = place_id
        self.photo_id = photo_id

def set_photo(place_id, image_file, folder):
    image_filename = uuid.uuid4().hex + ".jpg"
    image_file.save(os.path.join(app.config[folder], image_filename))
    description = image_filename                          

    # TODO: если записать в БД не удалось - удалить файл аватарки
    photo = Photo(description, place_id, image_filename)
    db.session.add(photo)
    db.session.commit()  


def delete_photo(ph_id, photo_id, folder):
    app.logger.debug("Deleting photo: ")	
    os.remove(os.path.join(app.config[folder], photo_id))

    photo = Photo.query.filter_by(id = ph_id, photo_id = photo_id).delete()	
    db.session.commit()

    return None	  