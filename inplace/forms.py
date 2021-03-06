# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField, SelectField, FileField, validators
from wtforms.widgets import TextArea
import re

class AvatarForm(Form):
    avatar = FileField(u'Выбрать основную фотографию')

###### TODO: Добавить недостающие поля формы.########
class PlaceForm(Form):
    name = StringField(u'Имя', [validators.InputRequired(), validators.Length(min = 1, max = 64)])
    description = StringField(u'Описание', [validators.InputRequired(), validators.Length(min = 3, max = 200)], widget=TextArea())
    avatar = FileField(u'Основная фотография места', [validators.Length(max = 64)])

class EventForm(Form):
    name = StringField(u'Имя', [validators.InputRequired(),validators.Length(max = 64)])
    description = StringField(u'Описание', [validators.InputRequired(),validators.Length(max = 64)], widget=TextArea())
    date = StringField(u'Дата', [validators.InputRequired(),validators.Length(max = 64)])
    photo = FileField(u'Основная фотография события')

class RegistrationForm(Form):
    login = StringField(u'Имя пользователя', [validators.Length(min=4, max=25)])
    name = StringField(u'Имя', [validators.InputRequired(), validators.Length(max = 128)])
    email = StringField(u'Эл. адрес', [validators.Email()])
    avatar = FileField(u'Изображение пользователя')
    password = PasswordField(u'Пароль', [
        validators.InputRequired(),
        validators.Length(max = 64),
        validators.EqualTo('confirm', message=u'Пароли должны совпадать')])
    confirm = PasswordField(u'Повторите пароль')

class LoginForm(Form):
    login = StringField(u'Имя пользователя', [validators.InputRequired(), validators.Length(max = 64)])
    password = PasswordField(u'Пароль', [validators.InputRequired(), validators.Length(max = 64)])

class SearchForm(Form):
    search_input = StringField([validators.Length(max = 64)])