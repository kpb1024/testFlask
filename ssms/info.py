from flask import (
    Blueprint, flash, g, session, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ssms.auth import login_required
from ssms.db import get_db

bp = Blueprint('info', __name__)

@bp.route('/')
@login_required
def index(check_author=True):
    sid = session['sid']
    score = get_db().execute(
        'SELECT cname, courseterm, coursepoint, score'
        ' FROM studentCourse sc JOIN course c ON sc.cid = c.cid'
        ' WHERE sc.sid = ?',
        (sid,)
    ).fetchall()

    if score is None:
        abort(404, "Student id {0} doesn't have Course score.".format(id))

    #if check_author and score['sid'] != g.user['sid']:
    #    abort(403)

    return render_template('info/index.html', scores=score)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        cname = request.form['cname']
        score = request.form['score']
        error = None

        if not cname:
            error = 'Course name is required.'
	elif not score:
	    error = 'Score is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
	    course = db.execute(
		'SELECT * FROM course WHERE cname = ? ', (cname,)
	    ).fetchone()
	    if course is None:
		error= 'Course do not exist'
                flash(error)
            db.execute(
                'INSERT INTO studentCourse (sid, cid, score)'
                ' VALUES (?, ?, ?)',
                (g.user['sid'], course['cid'], score)
            )
            db.commit()
            return redirect(url_for('info.index'))

    return render_template('info/create.html')

@bp.route('/createCourse', methods=('GET', 'POST'))
@login_required
def createCourse():
    """Create a new post for the current user."""
    if request.method == 'POST':
        cname = request.form['cname']
        courseterm = request.form['courseterm']
	coursepoint = request.form['coursepoint']
        error = None

        if not cname:
            error = 'Course name is required.'
	elif not courseterm:
	    error = 'Course term is required'
	elif not courseterm:
	    error = 'Course point is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO course (cname, courseterm, coursepoint)'
                ' VALUES (?, ?, ?)',
                (cname, courseterm, coursepoint)
            )
            db.commit()
            return redirect(url_for('info.index'))

    return render_template('info/createCourse.html')



#@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


#@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
