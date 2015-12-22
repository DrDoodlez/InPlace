# -*- coding: utf-8 -*-
from InPlace import app
from flask import render_template, request, url_for, redirect, session, flash, g
from .models import User, Place, Photo, authenticate_user, register_user, create_place, set_image, delete_old_image, set_photo
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
	photos = Photo.query.filter_by(place_id=place_id)
	return render_template('place.html', user = g.user, place = place, photos = photos)

@app.route('/place', methods = ["GET"])
def open_test_place():
	place = Place(u'Тестовое место', u'Данное место было взято не из базы... Смотрите реальные места на начальной странице')
	return render_template('place.html', place = place)

@app.route('/place/add', methods=["GET", "POST"])
def add_place():
	form = PlaceForm(request.form)
	# POST  - сохранение добавленого места
	if form.validate_on_submit():

		place = create_place(form.name.data, form.description.data)

		avatar_image = request.files[form.avatar.name]
		if avatar_image:
			app.logger.debug("Place image file: %s", avatar_image)
			set_image(place, avatar_image, 'AVATARS_FOLDER')
		
		uploaded_files = request.files.getlist("file[]")
		if uploaded_files[0]:
			for i in range(len(uploaded_files)):
				photo_image = uploaded_files[i]
				app.logger.debug("Setting images array  %s", uploaded_files)
				set_photo(place.id, photo_image, 'PHOTOS_FOLDER')

		return redirect('/place/' + str(place.id))

	return render_template('add_place.html', form = form)
	

@app.route('/place/add_user_place/<int:user_id>/<int:place_id>', methods=["GET", "POST"])
def add_user_place(user_id, place_id):
	add_place_to_user(user_id, place_id)

	return redirect("/place/" + str(place_id))

@app.route('/place/update/<int:place_id>', methods=["GET", "POST"])
def change_place(place_id):
	form = PlaceForm(request.form)
	place = Place.query.filter(Place.id == place_id).first()
	if form.validate_on_submit():
		app.logger.debug("Will update place: %s", place_id)	
		upd_place = update_place(place_id, form.name.data, form.description.data)
		app.logger.debug("Updated place: %s", place_id)
		
		avatar_image = request.files[form.avatar.name]
		if avatar_image and not place.avatar_id:	
			set_image(place, avatar_image, 'AVATARS_FOLDER')
		
		if avatar_image and place.avatar_id:
			app.logger.debug("Place image file update: %s", avatar_image)
			delete_old_image(place, 'AVATARS_FOLDER')
			app.logger.debug("Deleted image file, now updating ")
			set_image(place, avatar_image, 'AVATARS_FOLDER')

		uploaded_files = request.files.getlist("file[]")
		if uploaded_files[0]:
			for i in range(len(uploaded_files)):
				photo_image = uploaded_files[i]
				app.logger.debug("Setting images array  %s", uploaded_files)
				set_photo(place_id, photo_image, 'PHOTOS_FOLDER')

		upd_place = Place.query.filter(Place.id == place_id).first()
		form.name.data = upd_place.name
		form.description.data = upd_place.description
		form.avatar.data = upd_place.avatar_id

		return redirect('/place/' + str(upd_place.id))

	place = Place.query.filter(Place.id == place_id).first()
	form.name.data = place.name
	form.description.data = place.description	
	return render_template('update_place.html', form = form, id = place_id)



@app.route("/upload/<int:place_id>", methods=["POST"])
def load_updated_place(place_id):
	return redirect('/place/' + str(place_id)) 

##adds user avatar if it doesn't exsist
@app.route('/user/update/<int:user_id>', methods=["GET", "POST"])
def change_user_profile(user_id):
	form = AvatarForm(request.form)
	if form.validate_on_submit():
		user = User.query.get(int(user_id))

		avatar_image = request.files[form.avatar.name]
		if avatar_image and user.avatar_id:
			app.logger.debug("User image file update: %s", avatar_image)
			delete_old_image(user, 'AVATARS_FOLDER')
			app.logger.debug("Deleted image file, now updating ")
			set_image(user, avatar_image, 'AVATARS_FOLDER')
			app.logger.debug("Avatar '%s' successfully added", form.avatar.data)  

		if avatar_image and not user.avatar_id:	      
			set_image(user, avatar_image, 'AVATARS_FOLDER')
			app.logger.debug("Avatar '%s' successfully added", form.avatar.data) 

		return redirect('/user')	
	return render_template('update_user.html', form = form, id = user_id)


@app.route("/remove_photo/<int:photo_id>/<int:place_id>", methods=["POST"])
def remove_photo(photo_id):
	delete_photo(place_id)    	
	return redirect('/place/' + str(place_id)) #return render_template('update_place.html', files = uploaded_files, place_id= place_id)	
		

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


