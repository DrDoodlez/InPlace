# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, PasswordField, SelectField, validators

class CreateBoxForm(Form):
    name = StringField(u'Название Коробочки!', [validators.InputRequired()])
    # FIXME: генерировать список доступных цветов на основе модели
    color = SelectField(u'Цвет Коробочки!', choices=[("blue", u'Синий'),
                                                     ("red", u'Красный'),
                                                     ("green", u'Зеленый')])

class RegistrationForm(Form):
    login = StringField(u'Имя пользователя', [validators.Length(min=4, max=25)])
    name = StringField(u'Имя', [validators.InputRequired()])
    email = StringField(u'Эл. адрес', [validators.Email()])
    password = PasswordField(u'Пароль', [
        validators.InputRequired(),
        validators.EqualTo('confirm', message=u'Пароли должны совпадать')])
    confirm = PasswordField(u'Повторите пароль')

class LoginForm(Form):
    login = StringField(u'Имя пользователя', [validators.InputRequired()])
    password = PasswordField(u'Пароль', [validators.InputRequired()])
