from app import app, models, db
from flask import render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import PostForm, SignUpForm, LogInForm
import json

@app.route('/')
@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data)
		new_user = models.User(username=form.username.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		flash('Account successfully created! You will now be redirected to the login page!')
		return redirect(url_for('login'))
	return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LogInForm()
	if form.validate_on_submit():
		user = models.User.query.filter_by(username=form.username.data).first()
		if user and check_password_hash(user.password, form.password.data):
			flash('Successfully Logged In!')
			login_user(user)
			return(redirect(url_for('index')))
		else:
			flash("Invalid Username or Password. Please try again.")
	return render_template('login.html', form=form)

@app.route('/index', methods=['GET', 'POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		# Save post
		new_post = models.Post(text=form.post.data, user_id=current_user.id)
		db.session.add(new_post)
		db.session.commit()
	# Query after having added new post
	posts = models.Post.query.all()
	return render_template('index.html', form=form, posts=posts, username = current_user.username)

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
	post = models.Post.query.get_or_404(post_id)
	content = request.json.get('content')
	if not content or content.strip() == '':
		return jsonify({'error': 'Comment should not be empty'}), 400
	comment = models.Comment(text=content, post_id=post_id, user_id=current_user.id)
	db.session.add(comment)
	db.session.commit()
	return jsonify({'id' : comment.id, 'content' : comment.content, 'author' : current_user.username}), 201

# @csrf.exempt
@app.route('/vote', methods=['POST'])
def vote():
	data = json.loads(request.data)
	post_id = int(data.get('post_id'))
	post = models.Post.query.get(post_id)

	if data.get('vote_type') == "up":
		post.upvotes += 1
	else:
		post.downvotes += 1

	db.session.commit()
	return json.dumps({'status':'OK','upvotes': post.upvotes, 'downvotes': post.downvotes })