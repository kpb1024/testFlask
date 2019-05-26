from flask import (
	Blueprint, flash, g, session, redirect, render_template, request, url_for, current_app
)
from flask.json import jsonify
from werkzeug.exceptions import abort
from ssms.auth import login_required
from ssms.db import get_db, get_results
from ssms.student_analysis import *

bp = Blueprint('info', __name__)

@bp.route('/')
@login_required
def index(check_author=True):
	id = session['id']
	db = get_db()
	cur = db.cursor()
	cur.execute(
				'SELECT coursetype, cname, tname, courseyear, courseterm, coursepoint, score, gpa'
				' FROM studentCourse JOIN course'
				' WHERE sid = %s',
				(id)
		)
	courselist = get_results(cur)
	if courselist is None:
		abort(404, "Student id {0} doesn't have Course score.".format(id))

	return render_template('info/index.html', courses=courselist)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	"""Create a new post for the current user."""
	if request.method == 'POST':
		cname = request.form['cname']
		score = request.form['score']
		gpa = request.form['gpa']
		error = None

		if not cname:
			error = 'Course name is required.'
		elif not score:
			error = 'Score is required'

		if error is not None:
			flash(error)
		else:
			db = get_db()
			cur = db.cursor()
			cur.execute(
				'SELECT * FROM course WHERE cname = %s ', (cname)
			)
			course = get_results(cur)
			if len(course) is 0:
				error= 'Course do not exist'
				flash(error)
			db.execute(
				'INSERT INTO studentCourse (sid, cid, score, gpa)'
				' VALUES ( %s, %s, %s, %s)',
				(g.user['id'], course['cid'], score, gpa)
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
		coursetype = request.form['coursetype']	
		courseyear = request.form['courseyear']	
		tname = request.form['tname']	
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
			cur = db.cursor()
			cur.execute(
				'INSERT INTO course (cname, courseyear, coursetype, courseterm, coursepoint, tname)'
				' VALUES (%s, %s, %s, %s, %s, %s)',
				(cname, courseyear, coursetype, courseterm, coursepoint, tname)
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
	get_post(id)
	db = get_db()
	db.execute('DELETE FROM post WHERE id = ?', (id,))
	db.commit()
	return redirect(url_for('blog.index'))


@bp.route('/myScore', methods=('GET', 'POST'))
# @login_required
def myScore():
	sid = session['sid']
	cate = request.form['cate']
	term = request.form['term']
	scores = get_db().execute(
		'select courseName, score, GPA, render, entryStatus from Performances, Courses where studentNo=?'
		'and Performances.courseNo in (select courseNo from Courses where courseCate=? and courseTerm=?) and Performances.courseNo=Courses.courseNo', (sid, cate, term)).fetchall()
	if scores is None:
		abort(404, "Student id {0} doesn't have selected score.".format(sid))
	results = []
	for x in scores:
		results.append({'courseName': x[0], 'score': x[1], 'GPA': x[2], 'rank': x[3], 'entryStatus': x[4]})
	return render_template('info/myScore.html', scores=results)

@bp.route('/total_rank', methods=('GET', 'POST'))
@login_required		
def total_rank():
	total_rank = {}
	sid = session['id']
	total_rank['avg_coursetype'] = avg_coursetype(sid)
	total_rank['total_point'] = total_point(sid)
	total_rank['total_avg_gpa'] = total_avg_gpa(sid)
	return render_template('info/total_rank.html', scores=total_rank)


@bp.route('/term_rank', methods=('GET', 'POST'))
@login_required
def term_rank():
	sid = session['id']
	courseterm_rank = courseterm_rank(sid)
	courseterm = []
	rank = []
	for cr in courseterm_rank:
		courseterm.append(cr['courseterm'])
		rank.append(cr['totalrank'])
	return jsonify(term=courseterm, rnk=rank)


@bp.route('/score_pie', methods=('GET', 'POST'))
@login_required
def score_pie():
	sid = session['id']
	score_list = []
	distribution = score_distribution(sid)
	for score in distribution:
		score_dict = {}
		score_dict['name'] = list(score.keys())[0]
		score_dict['value'] = score.values()[0]
		score_list.append(score_dict)
		
	return jsonify(score_list)



	
	
