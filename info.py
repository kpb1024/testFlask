from flask import (
	Blueprint, flash, g, session, redirect, render_template, request, url_for, current_app
)
from flask.json import jsonify
from werkzeug.exceptions import abort
from ssms.auth import login_required
from ssms.db import get_db, get_results


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

@bp.route('/myAnalysis', methods=('GET', 'POST'))
@login_required	
def myAnalysis():
	sid = session['sid']
	
	analysis = get_db().execute(
		'select courseTerm, avg(score), max(score), min(score) from Performances, Courses where Performances.courseNo=Courses.courseNo')

@bp.route('/updateScore', methods=['GET', 'POST'])
@login_required
def updateScore():
	id=session['id']
	db =get_db()
	cur = db.cursor()
	cur.execute('select cid,cname,coursetype,coursepoint,coursevolume from course,teacher '
							 'where teacher.id=%s and teacher.name=course.tname',(id))
	courses = get_results(cur)
	return render_template('info/updateScore.html', courses=courses)
	

@bp.route('/importScore?cid=<cid>', methods=['GET', 'POST'])
@login_required
def importScore(cid):	
	tid = session['id']
	if request.method=="POST":
		db = get_db()
		cur = db.cursor()
		cur.execute('select sid,name from studentCourse,student where cid=%s and sid=student.id',(cid))
		Students=get_results(cur)
		for student in Students:
			dailyScore = request.form[str(student['sid'])]
			finalExamScore = request.form[student['name']]
			db.cursor().execute('update studentCourse set dailyScore=%s,finalExamScore=%s where sid=%s and cid=%s',(dailyScore,finalExamScore,student['sid'],cid))
		db.commit()
	db = get_db()
	cur = db.cursor()	
	cur.execute('select sid ,name,dailyScore,finalExamScore from student,studentCourse where cid=%s and sid=student.id', (cid))
	students=get_results(cur)
	return render_template('info/importScore.html', students=students,cid=cid)
	

@bp.route('/seeScore?cid=<cid>', methods=['GET', 'POST'])
@login_required
def seeScore(cid):
	if request.method == 'GET':
		tid = session['id']
		db = get_db()
		cur = db.cursor()
		cur.execute('update studentCourse set score = (dailyScore*dailyScoreRatio/100+finalExamScore*(100-dailyScoreRatio)/100) where cid=%s',(cid))
		cur1 = db.cursor()
		cur1.execute('select sid ,name,dailyScore,finalExamScore,score,status from student,studentCourse where cid=%s and sid=student.id',(cid))
		scores=get_results(cur1)	
		db.commit()
	return render_template('info/seeScore.html', scores=scores)
	
@bp.route('/setPercent?cid=<cid>', methods=['GET', 'POST'])
@login_required
def setPercent(cid):
	if request.method == 'POST':
		tid = session['id']
		dailyScoreRatio=request.form['dailyScoreRatio']
		db = get_db()
		db.cursor().execute('update studentCourse set dailyScoreRatio=%s where cid=%s',(dailyScoreRatio,cid))
		db.commit()
	db1 = get_db()
	cur1=db1.cursor()
	cur1.execute('select distinct dailyScoreRatio from studentCourse where cid=%s',(cid))
	per=get_results(cur1)
	db1.commit()
	return render_template('info/setPercent.html',cid=cid,per=per)	
	
@bp.route('/review', methods=['GET', 'POST'])
@login_required
def review():
	db = get_db()
	cur = db.cursor()
	cur.execute('select cid,cname,coursetype,coursepoint,coursevolume,tname from course,teacher')
	courses = get_results(cur)
	return render_template('info/review.html', courses=courses)
	
@bp.route('/reviewGrade?cid=<cid>', methods=['GET', 'POST'])
@login_required
def reviewGrade(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select sid ,name,dailyScore,finalExamScore,score,status from student,studentCourse where cid=%s and sid=student.id',(cid))
	scores=get_results(cur)
	return render_template('info/reviewGrade.html', scores=scores)