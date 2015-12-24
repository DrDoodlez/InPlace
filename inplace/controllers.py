# -*- coding: utf-8 -*-
from inplace import app
from flask import render_template, request, url_for, redirect, session, flash, g, abort
from .models import User, get_user, authenticate_user, register_user
from .models import Place, get_place, create_place, update_place, delete_place, find_place
from .models import Event, get_event, create_event, update_event, delete_event
from .models import Comment, get_comment, create_comment, update_comment, delete_comment
from .models import Photo, set_image, delete_old_image, allowed_file, set_photo, delete_photo
from .models import add_place_to_user, delete_place_from_user
from .models import add_event_to_place, delete_event_from_place, add_event_to_user, delete_event_from_user
from .models import add_comment_to_place, delete_comment_from_place
from .forms import  RegistrationForm, LoginForm, PlaceForm, SearchForm, EventForm, AvatarForm
from werkzeug import secure_filename


@app.route('/')
def index():
    places = Place.query
    return render_template('index.html', user = g.user, places = places)

@app.route('/place', methods = ["GET"])
def open_test_place():
    place = Place(u'Тестовое место', u'Данное место было взято не из базы... Смотрите реальные места на начальной странице')
    return render_template('place.html', place = place)

@app.route('/place/add', methods=["GET", "POST"])
def add_place():
    if not g.user:
        return redirect("/login")
    form = PlaceForm(request.form)
    # POST  - сохранение добавленого места
    if form.validate_on_submit():
        place = create_place(form.name.data, form.description.data)
        avatar_image = request.files[form.avatar.name]
        if avatar_image and allowed_file(avatar_image.filename):
            app.logger.debug("Place image file: %s", avatar_image)
            set_image(place, avatar_image, 'AVATARS_FOLDER')
        
        uploaded_files = request.files.getlist("file[]")
        if uploaded_files[0]:
            for i in range(len(uploaded_files)):
                if allowed_file(uploaded_files[i].filename):
                    photo_image = uploaded_files[i]
                    app.logger.debug("Setting images array  %s", uploaded_files)
                    set_photo(place.id, photo_image, 'PHOTOS_FOLDER')

        return redirect('/place/' + str(place.id))


    return render_template('add_place.html', form = form)

@app.route('/place/remove/<int:place_id>', methods=["GET", "POST"])
def remove_place(place_id):
    if not g.user:
        return redirect("/login")
    place = get_place(place_id)
    if not place: 
        request_text = u"Увы, нет такого места."
        abort(404, request_text)
    
    if not delete_place(place):
        request_text = u"Увы, не удалось удалить место."
        abort(404, request_text)
    return redirect('/')

@app.route('/place/<int:place_id>', methods = ["GET"])
def open_place(place_id):
    place = get_place(place_id)
    if not place:
        request_text = u"Увы, нет такого места."
        abort(404, request_text)
    photos = Photo.query.filter_by(place_id=place_id)
    events = place.events
    return render_template('place.html', user = g.user, place = place, 
        events = events, photos = photos)

@app.route('/search', methods = ["POST"])
def place_search():
    if g.searchForm.validate_on_submit():
        search_input = g.searchForm.search_input.data

        if search_input == "":
            return redirect('/')

        places = find_place(search_input)

        if places.count() == 0: 
             request_text = u"Увы, по вашему запросу ничего не найдено"
             return render_template('request_template.html',request_text = request_text)

        return render_template('index.html', user = g.user, places = places)
    return redirect('/')

# TODO: Использовать сессию
@app.route('/place/add_user_place/<int:user_id>/<int:place_id>', methods=["GET", "POST"])
def add_user_place(user_id, place_id):
    if not g.user:
        return redirect("/login")
    if g.user.id != user_id:
        request_text = u"Нельзя проводить операции над другими пользователями!!"
        abort(404, request_text)
    user = get_user(user_id)
    
    if not user:
        request_text = u"Увы, такого пользователя нет"
        abort(404, request_text)

    place = get_place(place_id)
    if not place:
        request_text = u"Увы, такого места нет"
        abort(404, request_text)
    
    if not add_place_to_user(user, place):
        request_text = u"Увы, не удалось добавить место"
        abort(404, request_text)
    return redirect("/place/" + str(place_id))

@app.route('/place/update/<int:place_id>', methods=["GET", "POST"])
def change_place(place_id):
    if not g.user:
        return redirect("/login")
    form = PlaceForm(request.form)
    place = get_place(place_id)
    if not place:
        request_text = u"Увы, такого нет места"
        abort(404, request_text)

    avatar_image = place.avatar_id
    if form.validate_on_submit():
        #place = get_place(place_id)
        app.logger.debug("Will update place: %s", place_id)
        if not place: 
            request_text = u"Увы, такого места нет"
            abort(404, request_text)
        
        upd_place = update_place(place, form.name.data, form.description.data)
        if not upd_place:
            request_text = u"Увы, не удалось изменить место"
            abort(404, request_text)

        app.logger.debug("Updated place: %s", place_id)
            
        avatar_image = request.files[form.avatar.name]
        if avatar_image and allowed_file(avatar_image.filename) and not place.avatar_id:    
            set_image(place, avatar_image, 'AVATARS_FOLDER')
        
        if avatar_image and allowed_file(avatar_image.filename) and place.avatar_id:
            app.logger.debug("Place image file update: %s", avatar_image)
            delete_old_image(place, 'AVATARS_FOLDER')
            app.logger.debug("Deleted image file, now updating ")
            set_image(place, avatar_image, 'AVATARS_FOLDER')

        uploaded_files = request.files.getlist("file[]")
        if uploaded_files[0]:
            for i in range(len(uploaded_files)):
                if allowed_file(uploaded_files[i].filename):
                    photo_image = uploaded_files[i]
                    app.logger.debug("Setting images array  %s", uploaded_files)
                    set_photo(place_id, photo_image, 'PHOTOS_FOLDER')

        upd_place = get_place(place_id)
        if not upd_place: 
            request_text = u"Увы, такого места нет (после обновления)"
            abort(404, request_text)

        form.name.data = upd_place.name
        form.description.data = upd_place.description
        form.avatar.data = upd_place.avatar_id

        return redirect('/place/' + str(place.id))

    form.name.data = place.name
    form.description.data = place.description

    return render_template('update_place.html', form = form, id = place_id)

@app.route("/upload/<int:place_id>", methods=["POST"])
def load_updated_place(place_id):
    return redirect('/place/' + str(place_id)) 

#########################
####### EVENT ###########
#########################

@app.route('/place/<int:place_id>/event/add', methods=["GET", "POST"])
def add_event(place_id):
    if not g.user:
        return redirect("/login")
    place = get_place(place_id)
    if not place:
        request_text = u"Увы, такого нет места"
        abort(404, request_text)

    form = EventForm(request.form)
    # POST  - сохранение добавленого места
    if form.validate_on_submit():

        ###### TODO: Нужно доделать добавление фотографии месту.########
        #photo = request.files[form.photo.name]
        event = create_event(form.name.data, form.description.data, form.date.data)
        if not add_event_to_place(place, event):
            request_text = u"Увы, не удалось добавить событие"
            abort(404, request_text)
        
        return redirect("/place/" + str(place_id))

    return render_template('add_event.html', form = form, place_id = place_id)

@app.route('/event/add_user_event/<int:user_id>/<int:event_id>', methods=["GET", "POST"])
def add_user_event(user_id, event_id):
    if not g.user:
        return redirect("/login")
    if g.user.id != user_id:
        request_text = u"Нельзя проводить операции над другими пользователями!!"
        abort(404, request_text)

    user = get_user(user_id)
    if not user:
        request_text = u"Увы, такого нет пользователя"
        abort(404, request_text)
    
    event = get_event(event_id)
    if not event:
        request_text = u"Увы, такого нет события"
        abort(404, request_text)       

    if not add_event_to_user(user, event):
        request_text = u"Увы, не удалось добавить событие"
        abort(404, request_text)

    return redirect("/event/" + str(event_id))

@app.route('/user/remove_event/<int:user_id>/<int:event_id>', methods = ["GET", "POST"])
def remove_event_from_user(user_id, event_id):
    if not g.user:
        return redirect("/login")
    if g.user.id != user_id:
        request_text = u"Нельзя проводить операции над другими пользователями!!"
        abort(404, request_text)

    user = get_user(user_id)
    if not user:
        request_text = u"Увы, такого нет пользователя"
        abort(404, request_text)
    
    event = get_event(event_id)
    if not event:
        request_text = u"Увы, такого нет события"
        abort(404, request_text)

    if not delete_event_from_user(user, event):
        request_text = u"Увы, не удалось удалить событие"
        abort(404, request_text)
    return redirect('/user')

@app.route('/user/remove_event_2/<int:user_id>/<int:event_id>', methods = ["GET", "POST"])
def remove_event_from_user_2(user_id, event_id):
    if not g.user:
        return redirect("/login")
    if g.user.id != user_id:
        request_text = u"Нельзя проводить операции над другими пользователями!!"
        abort(404, request_text)

    user = get_user(user_id)
    if not user:
        request_text = u"Увы, такого нет пользователя"
        abort(404, request_text)
    
    event = get_event(event_id)
    if not event:
        request_text = u"Увы, такого нет события"
        abort(404, request_text)
        
    if not delete_event_from_user(user, event):
        request_text = u"Увы, не удалось удалить событие"
        abort(404, request_text)
    return redirect("/event/" + str(event_id))

@app.route('/event/<int:event_id>', methods = ["GET"])
def open_event(event_id):
    event = get_event(event_id)
    if not event:
        request_text = u"Увы, такого нет события"
        abort(404, request_text)
    return render_template('event.html', user = g.user, event = event)

@app.route('/event/update/<int:event_id>', methods=["GET", "POST"])
def change_event(event_id):
    if not g.user:
        return redirect("/login")
    event = get_event(event_id)
    if not event:
        request_text = u"Увы, такого нет события"
        abort(404, request_text)

    form = EventForm(request.form)
    if form.validate_on_submit():
        ###### TODO: Нужно доделать добавление фотографии месту.########
        #photo = request.files[form.photo.name]
        print "Controller: %s %s %s" % (form.name.data, form.description.data, form.date.data)
        if not update_event(event, form.name.data, form.description.data, form.date.data):
            request_text = u"Увы, не удалось изменить событие"
            abort(404, request_text)
        
        return redirect("/event/" + str(event_id))

    form.name.data = event.name
    form.description.data = event.description
    form.date.data = event.date

    return render_template('update_event.html', form = form, id = event.id)

@app.route('/event/remove/<int:event_id>', methods=["GET", "POST"])
def remove_event(event_id):
    if not g.user:
        return redirect("/login")
    event = get_event(event_id)
    if not event:
        request_text = u"Увы, такого нет события"
        abort(404, request_text)
    
    if not delete_event(event):
        request_text = u"Увы, не удалось удалить событие"
        abort(404, request_text)    
    return redirect('/')

@app.route('/user', methods = ["GET", "POST"])
def open_user():
    user = g.user
    if not user:
        return redirect("/login")
    places = user.places
    events = user.events
    return render_template('user.html', user = user, places = places, events = events)

##adds user avatar if it doesn't exsist
@app.route('/user/update/<int:user_id>', methods=["GET", "POST"])
def change_user_profile(user_id):
    if not g.user:
        return redirect("/login")
    if g.user.id != user_id:
        request_text = u"Нельзя проводить операции над другими пользователями!!"
        abort(404, request_text)

    user = get_user(user_id)
    if not user:
        request_text = u"Увы, такого пользователя нет"
        abort(404, request_text)

    form = AvatarForm(request.form)
    if form.validate_on_submit():
        avatar_image = request.files[form.avatar.name]
        app.logger.debug("User image filename: %s", allowed_file(avatar_image.filename))

        if avatar_image and allowed_file(avatar_image.filename) and user.avatar_id:
            app.logger.debug("User image file update: %s", avatar_image)
            delete_old_image(user, 'AVATARS_FOLDER')
            app.logger.debug("Deleted image file, now updating ")
            set_image(user, avatar_image, 'AVATARS_FOLDER')
            app.logger.debug("Avatar '%s' successfully added", form.avatar.data)  

        if avatar_image and allowed_file(avatar_image.filename) and not user.avatar_id:       
            set_image(user, avatar_image, 'AVATARS_FOLDER')
            app.logger.debug("Avatar '%s' successfully added", form.avatar.data) 

        return redirect('/user')    
    return render_template('update_user.html', form = form, id = user_id)

@app.route("/remove_photo/<int:place_id>/<int:ph_id>/<photo_id>", methods=["GET", "POST"])
def remove_photo(ph_id, place_id, photo_id):
    if not g.user:
        return redirect("/login")
    delete_photo(ph_id, photo_id, 'PHOTOS_FOLDER')      
    return redirect('/place/' + str(place_id)) #return render_template('update_place.html', files = uploaded_files, place_id= place_id) 
        

@app.route('/user/remove_place/<int:user_id>/<int:place_id>', methods = ["GET", "POST"])
def remove_place_from_user(user_id, place_id):
    if not g.user:
        return redirect("/login")
    if g.user.id != user_id:
        request_text = u"Нельзя проводить операции над другими пользователями!!"
        abort(404, request_text)

    user = get_user(user_id)
    if not user:
        request_text = u"Увы, такого пользователя нет"
        abort(404, request_text)
    
    place = get_place(place_id)
    if not place:
        request_text = u"Увы, такого места нет"
        abort(404, request_text)

    if not delete_place_from_user(user, place):
        request_text = u"Не удалось удалить место"
        abort(404, request_text)
    return redirect('/user')

@app.route('/user/remove_place_2/<int:user_id>/<int:place_id>', methods = ["GET", "POST"])
def remove_place_from_user_2(user_id, place_id):
    if not g.user:
        return redirect("/login")
    if g.user.id != user_id:
        request_text = u"Нельзя проводить операции над другими пользователями!!"
        abort(404, request_text)

    user = get_user(user_id)
    if not user:
        request_text = u"Увы, такого пользователя нет"
        abort(404, request_text)
    
    place = get_place(place_id)
    if not place:
        request_text = u"Увы, такого места нет"
        abort(404, request_text)

    if not delete_place_from_user(user, place):
        request_text = u"Не удалось удалить место"
        abort(404, request_text)
    return redirect("/place/" + str(place_id))

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
        if not user:
            request_text = u"Увы, пользователь с таким логином или почтой уже существует. "
            return render_template('request_template.html',request_text = request_text)
        set_image(user, avatar_image, 'AVATARS_FOLDER')

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
    g.searchForm = SearchForm(request.form)
    if 'user_id' not in session:        
        return
    
    user_id = session['user_id']

    #TODO: проверить существует ли такой пользователь и может ли он
    #работать с системой
    g.user = User.query.get(int(user_id))


## Код для перехвата ошибки... Пока не нужно, просто передаём текст ошибки в аборт.
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
