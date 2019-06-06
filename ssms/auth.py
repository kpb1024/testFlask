import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from ssms.db import get_db, get_results

bp = Blueprint('auth', __name__)

def login_required(view):
	"""View decorator that redirects anonymous users to the login page."""
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view

def teacher_required(view):
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
		elif g.user['auth'] is not 1:
			flash('Only teachers are permitted to do this.')

		return view(**kwargs)

	return wrapped_view


@bp.before_app_request
def load_logged_in_user():
	"""If a user id is stored in the session, load the user object from
	the database into ``g.user``."""
	id = session.get('id')

	if id is None:
		g.user = None
	else:
		cur = get_db().cursor()
		cur.execute(
			'SELECT * FROM user WHERE id = %s', (id)
		)
		g.user = get_results(cur)[0]


@bp.route('/register', methods=('GET', 'POST'))
def register():
	"""Register a new user.
	Validates that the username is not already taken. Hashes the
	password for security.
	
	Use cursor to execute SQL query.
	"""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		id = request.form['id']
		sname	 = request.form['sname']
		auth = request.form['auth']
		is_male = request.form['is_male']
		cur = get_db().cursor()
		error = None
		if cur.execute('SELECT id FROM user WHERE username = %s', (username)) is not 0:
			error = 'NetID {0} is already registered.'.format(username)
		if error is None:
			cur.execute(
				'INSERT INTO user (id, username, password, auth, is_male) VALUES (%s, %s, %s, %s, %s)',
				(id, username,	generate_password_hash(password), auth, is_male)
			)
			cur.execute(
				'INSERT INTO student (id, name) VALUES (%s, %s)',
				(id, sname)
		)
			db.commit()
			return redirect(url_for('auth.login'))
		flash(error)

	return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
	"""Log in a registered user by adding the user id to the session."""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		cur = db.cursor()
		error = None
		cur.execute(
			'SELECT * FROM user WHERE username = %s', (username,)
		)
		#user = cur.fetchone()
		user = get_results(cur)
		if len(user) is 0:
			error = 'Incorrect username.'
		elif not check_password_hash(user[0]['password'], password):
			error = 'Incorrect password.'

		if error is None:
			# store the user id in a new session and return to the index
			session.clear()
			session['id'] = user[0]['id']
			session['username'] = user[0]['username']
			session['auth'] = user[0]['auth']
			return redirect(url_for('info.index'))

		flash(error)

	return render_template('auth/login.html')

@bp.route('/logout')
def logout():
	"""Clear the current session, including the stored user id."""
	session.clear()
	return redirect(url_for('index'))
