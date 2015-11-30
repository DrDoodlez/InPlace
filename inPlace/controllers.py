# -*- coding: utf-8 -*-
from InPlace import app
from flask import render_template, request, url_for, redirect, session, flash, g
from .models import Box, User, Place, authenticate_user, register_user, create_box, set_user_avatar, create_place
from .forms import CreateBoxForm, RegistrationForm, LoginForm, CreatePlaceForm
from werkzeug import secure_filename


@app.route('/')
def index():
    return render_template('index.html', user=g.user, places=Place.query)

@app.route('/search')
def openSearch():        
    return render_template('search.html')

#TODO: Добавить передачу модели, для открытия конкретного места
@app.route('/place', methods=["GET", "POST"])
def open_place():
    return render_template('place.html')

@app.route('/add', methods=["GET", "POST"])
def add_place():
    form = CreatePlaceForm(request.form)

    # POST  - сохранение добавленого места
    if form.validate_on_submit():

        ###### TODO: Нужно доделать добавление фотографии месту.########
        photo = request.files[form.photo.name]
        place = create_place(form.name.data, form.description.data)
        
        return redirect('/')

    return render_template('add_place.html', form = form)


# TODO: Add new routes
# @app.route('/boxes', methods=["GET", "POST"])
# def inPlace_list():
#     form = CreateBoxForm(request.form)
    
#     if g.user:
#         boxes = g.user.boxes
#     else:
#         flash(u'Чтобы просматривать список Коробочек!™ вам необходимо войти в систему')
#         return redirect('/login')
    
#     if form.validate_on_submit():
#         # TODO: обработать ошибки добавления новой коробочки
#         box = create_box(g.user, form.name.data, form.color.data)
        
#         return redirect('/boxes')
    
#     return render_template('boxes.html', boxes=boxes, form=form)

@app.route('/register', methods=["GET", "POST"])
def registration():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        app.logger.debug("Going to register a user with login '%s' and password '%s'",
                    form.login.data, form.password.data)

        avatar_image = request.files[form.avatar.name]
        app.logger.debug("User image file: %s", avatar_image)
       

        # TODO: обработать ошибки добавления нового пользователя        
        user = register_user(form.login.data, form.email.data, form.name.data, form.password.data)
        set_user_avatar(user, avatar_image)

        app.logger.debug("User '%s' successfully registered", user.login)        
        flash(u'Пользователь %s успешно зарегистрирован.' % form.login.data)
        
        return redirect('/login')
        
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = authenticate_user(form.login.data, form.password.data)
        if user:
            session["user_id"] = user.id
            return redirect('/')
        else:
            flash(u'Неверное имя пользователя или пароль')
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.before_request
def verify_user_session():
    g.user = None
    
    if 'user_id' not in session:        
        return
    
    user_id = session['user_id']

    #TODO: проверить существует ли такой пользователь и может ли он
    #работать с системой
    g.user = User.query.get(int(user_id))
