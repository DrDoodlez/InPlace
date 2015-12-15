# -*- coding: utf-8 -*-
from InPlace import app
from flask import render_template, request, url_for, redirect, session, flash, g
from .models import Box, User, Place, authenticate_user, register_user, create_box, set_user_avatar, create_place, update_place, delete_place, add_place_to_user, delete_place_from_user
from .forms import CreateBoxForm, RegistrationForm, LoginForm, PlaceForm
from werkzeug import secure_filename


@app.route('/')
def index():
    places = Place.query
    return render_template('index.html', user = g.user, places = places)

@app.route('/search')
def open_search():        
    return render_template('search.html')

#TODO: Добавить передачу модели, для открытия конкретного места
@app.route('/place/<int:place_id>', methods = ["GET"])
def open_place(place_id):
    place = Place.query.get(place_id)
    return render_template('place.html', user = g.user, place = place)

@app.route('/place', methods = ["GET"])
def open_test_place():
    place = Place(u'Тестовое место', u'Данное место было взято не из базы... Смотрите реальные места на начальной странице')
    return render_template('place.html', place = place)

@app.route('/place/add', methods=["GET", "POST"])
def add_place():
    form = PlaceForm(request.form)
    # POST  - сохранение добавленого места
    if form.validate_on_submit():

        ###### TODO: Нужно доделать добавление фотографии месту.########
        #photo = request.files[form.photo.name]
        place = create_place(form.name.data, form.description.data)
        
        return redirect('/')

    return render_template('add_place.html', form = form)

@app.route('/place/add_user_place/<int:user_id>/<int:place_id>', methods=["GET", "POST"])
def add_user_place(user_id, place_id):
	add_place_to_user(user_id, place_id)

	return redirect("/place/" + str(place_id))

@app.route('/place/update/<int:place_id>', methods=["GET", "POST"])
def change_place(place_id):
    form = PlaceForm(request.form)
    if form.validate_on_submit():
        ###### TODO: Нужно доделать добавление фотографии месту.########
        #photo = request.files[form.photo.name]
        print "Controller:   %s %s" % (form.name.data, form.description.data)
        update_place(place_id, form.name.data, form.description.data)
        
        return redirect('/')

    place = Place.query.filter(Place.id == place_id).first()
    form.name.data = place.name
    form.description.data = place.description

    return render_template('update_place.html', form = form, id = place_id)

@app.route('/place/remove/<int:place_id>', methods=["GET", "POST"])
def remove_place(place_id):
    delete_place(place_id)    
    return redirect('/')

@app.route('/user', methods = ["GET", "POST"])
def open_user():
    user = g.user
    # места нужно получать из списка мест пользователя
    places = user.places
    #places = JoinUserPlace.query.filter_by(userId = user.Id).args.get(placeId)
    return render_template('user.html', user = user, places = places)

# TODO: реализовать удаление места из списка 
# и возвращение к странице пользователя.
@app.route('/user/remove_place/<int:user_id>/<int:place_id>', methods = ["GET", "POST"])
def remove_place_from_user(user_id, place_id):
    delete_place_from_user(user_id, place_id)
    return redirect('/user')

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
