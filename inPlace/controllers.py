# -*- coding: utf-8 -*-
from InPlace import app
from flask import render_template, request, url_for, redirect, session, flash, g
from .models import User, Place, authenticate_user, register_user, set_user_avatar, create_place, set_place_avatar
from .models import update_place, delete_place, add_place_to_user, delete_place_from_user, find_place, create_event, update_event, delete_event
from .forms import  RegistrationForm, LoginForm, PlaceForm, SearchForm, AvatarForm
from werkzeug import secure_filename


@app.route('/')
def index():
	places = Place.query
	return render_template('index.html', user = g.user, places = places)

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
		avatar_image = request.files[form.avatar.name]

		place = create_place(form.name.data, form.description.data)
		set_place_avatar(place, avatar_image)
		app.logger.debug("Place image file: %s", avatar_image)
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
		#print "Controller:   %s %s" % (form.name.data, form.description.data, form.avatar.data)
		#avatar_image = request.files[form.avatar.name]
    	#app.logger.debug("Place image file: %s", avatar_image)
	    update_place(place_id, form.name.data, form.description.data)
	    place = Place.query.filter(Place.id == place_id).first()

	    form.name.data = place.name
	    form.description.data = place.description
	    
	    return redirect('/')
	return render_template('update_place.html', form = form, id = place_id)


##adds user avatar if it doesn't exsist
@app.route('/user/<int:user_id>', methods=["GET", "POST"])
def add_user_avatar(user_id):

	form = AvatarForm(request.form)
	app.logger.debug(" recieved form")
	if form.validate_on_submit():
		app.logger.debug("Going to add avatar to user with id '%s'", form.avatar.data)

		avatar_image = request.files[form.avatar.name]
		app.logger.debug("User image file: %s", avatar_image)
	   
		# TODO: обработать ошибки добавления нового пользователя        
		user = User.query.get(int(user_id))
		set_user_avatar(user, avatar_image)
			
		app.logger.debug("Avatar '%s' successfully added", form.avatar.data)        
		flash(u'Пользователю успешно добавлена ава.' % form.avatar.data)
		
	#return open_user()
	#return redirect('/user')
	return render_template('user.html', user = user)
	return render_template('user.html', user = user)

		

@app.route('/place/remove/<int:place_id>', methods=["GET", "POST"])
def remove_place(place_id):
	delete_place(place_id)    
	return redirect('/')

@app.route('/user', methods = ["GET", "POST"])
def open_user():
	user = g.user
	places = user.places
	return render_template('user.html', user = user, places = places)

@app.route('/user/remove_place/<int:user_id>/<int:place_id>', methods = ["GET", "POST"])
def remove_place_from_user(user_id, place_id):
	delete_place_from_user(user_id, place_id)
	return redirect('/user')

@app.route('/user/remove_place_2/<int:user_id>/<int:place_id>', methods = ["GET", "POST"])
def remove_place_from_user_2(user_id, place_id):
	delete_place_from_user(user_id, place_id)
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
	g.searchForm = SearchForm(request.form)
	if 'user_id' not in session:        
		return
	
	user_id = session['user_id']

	#TODO: проверить существует ли такой пользователь и может ли он
	#работать с системой
	g.user = User.query.get(int(user_id))


