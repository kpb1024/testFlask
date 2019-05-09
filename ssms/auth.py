import functools

from flask import (
<<<<<<< HEAD
    Blueprint, flash, g, redirect, render_template, request, session, url_for
=======
	Blueprint, flash, g, redirect, render_template, request, session, url_for
>>>>>>> 266f41eeae4d225dbf423f5cf25d955d8177b373
)
from werkzeug.security import check_password_hash, generate_password_hash

from ssms.db import get_db

bp = Blueprint('auth', __name__)


def login_required(view):
<<<<<<< HEAD
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
=======
	"""View decorator that redirects anonymous users to the login page."""
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view
>>>>>>> 266f41eeae4d225dbf423f5cf25d955d8177b373


@bp.before_app_request
def load_logged_in_user():
<<<<<<< HEAD
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user JOIN student WHERE id = ?', (user_id,)
        ).fetchone()
=======
	"""If a user id is stored in the session, load the user object from
	the database into ``g.user``."""
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user JOIN student WHERE id = ?', (user_id,)
		).fetchone()
>>>>>>> 266f41eeae4d225dbf423f5cf25d955d8177b373


@bp.route('/register', methods=('GET', 'POST'))
def register():
<<<<<<< HEAD
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
	sid      = request.form['sid']
	sname    = request.form['sname']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not sid:
            error = 'Student ID is required.'
        elif not sname:
            error = 'Your name is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'NetID {0} is already registered.'.format(username)
        elif db.execute(
            'SELECT sid FROM student WHERE sid = ?', (sid,)
        ).fetchone() is not None:
            error = 'Student ID {0} is already registered.'.format(sid)

        if error is None:
            # the name and student ID is available, store it in the database and go to
            # the login page
	    # auth = 0 for student
            db.execute(
                'INSERT INTO user (username, password, auth) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), 0)
            )
            db.execute(
                'INSERT INTO student (sid, sname, uid) VALUES (?, ?,  (SELECT last_insert_rowid()))',
                (sid, sname)
	    )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
=======
	"""Register a new user.

	Validates that the username is not already taken. Hashes the
	password for security.
	"""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		sid		 = request.form['sid']
		sname	 = request.form['sname']
		db = get_db()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif not sid:
			error = 'Student ID is required.'
		elif not sname:
			error = 'Your name is required.'
		elif db.execute(
			'SELECT id FROM user WHERE username = ?', (username,)
		).fetchone() is not None:
			error = 'NetID {0} is already registered.'.format(username)
		elif db.execute(
			'SELECT sid FROM student WHERE sid = ?', (sid,)
		).fetchone() is not None:
			error = 'Student ID {0} is already registered.'.format(sid)

		if error is None:
			# the name and student ID is available, store it in the database and go to
			# the login page
		# auth = 0 for student
			db.execute(
				'INSERT INTO user (username, password, auth) VALUES (?, ?, ?)',
				(username, generate_password_hash(password), 0)
			)
			db.execute(
				'INSERT INTO student (sid, sname, uid) VALUES (?, ?,  (SELECT last_insert_rowid()))',
				(sid, sname)
		)
			db.commit()
			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')
>>>>>>> 266f41eeae4d225dbf423f5cf25d955d8177b373


@bp.route('/login', methods=('GET', 'POST'))
def login():
<<<<<<< HEAD
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
	student = db.execute(
            'SELECT * FROM student WHERE uid = ?', (user['id'],)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
	    session['sid'] = student['sid']
            return redirect(url_for('info.index'))

        flash(error)

    return render_template('auth/login.html')
=======
	"""Log in a registered user by adding the user id to the session."""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
		).fetchone()
		student = db.execute(
			'SELECT * FROM student WHERE uid = ?', (user['id'],)
		).fetchone()

		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			# store the user id in a new session and return to the index
			session.clear()
			session['user_id'] = user['id']
			session['sid'] = student['sid']
			return redirect(url_for('info.index'))

		flash(error)

	return render_template('auth/login.html')
>>>>>>> 266f41eeae4d225dbf423f5cf25d955d8177b373


@bp.route('/logout')
def logout():
<<<<<<< HEAD
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('index'))
=======
	"""Clear the current session, including the stored user id."""
	session.clear()
	return redirect(url_for('index'))
>>>>>>> 266f41eeae4d225dbf423f5cf25d955d8177b373
