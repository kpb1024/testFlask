#!/usr/bin/python
#coding:utf-8

from flask import (
	Blueprint, flash, g, session, redirect, render_template, request, url_for, current_app
)
from flask.json import jsonify
from werkzeug.exceptions import abort
from ssms.auth import login_required
from ssms.db import get_db, get_results
from ssms.analysis import * 

bp = Blueprint('info', __name__)

@bp.route('/', methods=('GET','POST'))
@login_required
def index():
	if session['auth'] == 1:
		id=session['id']
		db =get_db()
		cur = db.cursor()
		sql='select course.cid,cname,dailyScoreRatioDesc,coursepoint,courseyear,courseterm,scoreType,scoreReviewStatus from course,teacher,studentCourse  where teacher.id=%s and teacher.id=course.tid and teacher.id=studentCourse.tid and studentCourse.cid=course.cid'% id
		if request.method == 'POST':
			year = request.form['courseyear']
			term = request.form['courseterm']
			if year == u'' and term == u'':
				pass
			if year is not u'':
				sql += ' and courseyear = %s' % year
			if term is not u'':
				sql += ' and courseterm = %s' % term
			cur.execute(sql)
			courses = get_results(cur)
			return render_template('info/index2.html', courses=courses)
		cur.execute(sql)
		courses = get_results(cur)
		return render_template('info/index2.html', courses=courses)
	id = session['id']
	db = get_db()
	cur = db.cursor()
	total_rank = {}
	total_rank['avg_coursetype'] = avg_coursetype(id)
	total_rank['total_point'] = total_point(id)
	total_rank['total_avg_gpa'] = total_avg_gpa(id)
	courseClass= {}
	for i in range(len(courseclass_gpa_rank(id))):
	    ctype=courseclass_gpa_rank(id)[i]['courseclass']
	    courseClass[ctype]=courseclass_gpa_rank(id)[i]
	sql = 'SELECT coursetype, cname, t.name, courseyear, courseterm, coursepoint, score, gpa,`scoreReviewStatus` st, studentExamStatus '
	sql += 'FROM studentCourse sc JOIN course c JOIN teacher t where sc.tid = t.id and sc.cid = c.cid and '
	sql += 'sid = %s' % id
	if request.method == 'POST':
		type = request.form['coursetype']
		year = request.form['courseyear']
		term = request.form['courseterm']
		if type == u'' and year == u'' and term == u'':
			pass
		if type is not u'':
			sql += ' and coursetype = \'%s\'' % type
		if year is not u'':
			sql += ' and courseyear = %s' % year
		if term is not u'':
			sql += ' and courseterm = %s' % term
		cur.execute(sql)
		courselist = get_results(cur)
		return render_template('info/index.html', courses=courselist, scores=total_rank, cc=courseClass)
	cur.execute(sql)
	courselist = get_results(cur)
	if len(courselist) is 0:
		abort(404, "Student id {0} doesn't have Course score.".format(id))
	courseClass= {}
	for i in range(len(courseclass_gpa_rank(id))):
	    ctype=courseclass_gpa_rank(id)[i]['courseclass']
	    courseClass[ctype]=courseclass_gpa_rank(id)[i]
	return render_template('info/index.html', courses=courselist, scores=total_rank,cc=courseClass)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
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
	if request.method == 'POST':
		cname = request.form['cname']
		courseterm = request.form['courseterm']
		coursepoint = request.form['coursepoint']
		coursetype = request.form['coursetype']
		coursevolume = request.form['coursevolume']
		courseyear = request.form['courseyear']
		courseclass = request.form['courseclass']
		scoreType = request.form['scoreType']
		dailyScoreRatio = request.form['dailyScoreRatio']
		dailyScoreRatioDesc = request.form['dailyScoreRatioDesc']
		tid = g.user['id']
		db = get_db()
		cur = db.cursor()
		cur.execute(
			'INSERT INTO course VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
			(cname, courseterm, courseyear, coursepoint, coursetype, coursevolume, tid, dailyScoreRatio, dailyScoreRatioDesc, courseclass, scoreType)
		)
		db.commit()
		return redirect(url_for('info.index'))

	return render_template('info/createCourse.html')

@bp.route('/proposal', methods=('GET', 'POST'))
@login_required
def proposal():
	db = get_db()
	cur = db.cursor()
	cur.execute(
		'SELECT distinct course.cid, cname'
        ' FROM studentCourse JOIN course'
        ' WHERE sid = %s',
		(g.user['id'])
	)
	courses = get_results(cur)
	db.commit()
	if request.method == 'POST':
		cid = request.form['course']
		reason = request.form['reason']
		error = None
		if not cid:
			error = 'Course name is required.'
		elif not reason:
			error = 'Reason is required'
		if error is not None:
			flash(error)
		else:
			db = get_db()
			cur = db.cursor()
			cur.execute(
			'INSERT INTO proposal(sid, cid, reason)'
			'values(%s, %s, %s)'
			, (g.user['id'], cid, reason)
			)
			db.commit()
			flash('成功提交！')
			return redirect(url_for('info.showProposal'))
	
	return render_template('info/proposal.html', courses = courses)

@bp.route('/showProposal', methods=('GET', 'POST'))
@login_required
def showProposal():
	db = get_db()
	cur = db.cursor()
	id = g.user['id']
	sql = 'select DISTINCT cname,raisedTime,score, reason, reply,is_checked_by_teacher, is_checked_by_dean,course.cid  from proposal, course,studentCourse where course.cid = studentCourse.cid and proposal.cid=course.cid  and proposal.sid = studentCourse.sid'
	if g.user['auth'] == 0:
		sql += ' and proposal.sid =%s' % id
		cur.execute(sql)
	else:
		sql += ' and proposal.cid =%s'
		cur.executemany(sql, g.user['cid'])
	proposals = get_results(cur)
	return render_template('info/showProposal.html', proposals = proposals)



@bp.route('/cancelProposal/<cid>')
@login_required
def cancelProposal(cid):
	cur = get_db().cursor()
	id = g.user['id']
	cur.execute('delete from proposal where cid = %s and sid = %s', cid, id)
	redirect(url_for('info.index'))

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

@bp.route('/term_gpa', methods=('GET', 'POST'))
@login_required
def term_gpa():
	sid = session['id']
	term_gpa = term_avg_gpa(sid)
	courseterm = []
	courseyear = []
	gpa=[]
	for tg in term_gpa:
		gpa.append(tg['gp'])
		courseyaer.append(tg['courseyear'])
		courseterm.append(tg['courseterm'])
	return jsonify(term=courseterm, year=courseyaer, gpa=gpa)

@bp.route('/term_rank', methods=('GET', 'POST'))
@login_required
def term_rank():
	sid = session['id']
	term_rank = courseterm_rank(sid)
	courseterm = []
	rank = []
	for cr in term_rank:
		courseterm.append(cr['courseterm'])
		rank.append(cr['totalrank'])
	print(courseterm)
	print(rank)
	return jsonify(term=courseterm, rnk=rank)


@bp.route('/score_pie', methods=('GET', 'POST'))
@login_required
def score_pie():
	sid = session['id']
	score_list = []
	distribution = score_distribution(sid)
	for score in distribution:
		if list(score.values())[0] != 0:
			score_dict = {}
			score_dict['name'] = list(score.keys())[0]
			score_dict['value'] = list(score.values())[0]
			score_list.append(score_dict)
		
	return jsonify(score_list)

@bp.route('/sw_analysis', methods=('GET', 'POST'))
@login_required
def sw_analysis():
	sid = session['id']
	sw_list = {}
	s_list = []
	tp_subject = top_subject(sid)
	for subject in tp_subject:
		course = {}
		course['cname'] = subject['cname']
		course['score'] = subject['score']
		course['gpa'] = subject['gpa']
		course['course_count'] = course_count(subject['cid'])[0]['count']
		course['course_avg'] = course_avg(subject['cid'])[0]['avg']
		course['student_rank'] = student_rank(subject['cid'], sid)[0]['rnk']
		s_list.append(course)
	sw_list['s_list'] = s_list
	w_list = []
	wt_subject = worst_subject(sid)
	for subject in wt_subject:
		course = {}
		course['cname'] = subject['cname']
		course['score'] = subject['score']
		course['gpa'] = subject['gpa']
		course['course_count'] = course_count(subject['cid'])[0]['count']
		course['course_avg'] = course_avg(subject['cid'])[0]['avg']
		course['student_rank'] = student_rank(subject['cid'], sid)[0]['rnk']
		w_list.append(course)
	sw_list['w_list'] = w_list
	return render_template('info/sw_analysis.html', sw_list=sw_list)


@bp.route('/sco_distribution', methods=('GET', 'POST'))
@login_required
def sco_distribution():
	sid = session['id']
	involve = course_involve(sid)
	courses = []
	for course in involve:
		cid = course['cid']
		subject = {}
		c = course_info(cid)
		subject['cid'] = cid
		subject['cname'] = course['cname']
		subject['avg'] = c[0]['avg']
		subject['max'] = c[0]['max']
		subject['good'] = c[0]['good']
		courses.append(subject)
	return render_template('info/score_distribution.html', courses=courses)


@bp.route('/score_distribution_graph/<cid>', methods=('GET', 'POST'))
@login_required
def score_distribution_graph(cid):
	score_dis = course_score(cid)
	score = {}
	range = []
	count = []
	for s in score_dis:
		for key, value in s.items():
			range.append(key)
			count.append(value)
	score['range'] = range
	score['count'] = count
	return jsonify(score)

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
	CourseId = cid
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
		return redirect(url_for('info.seeScore',cid=CourseId))
	db = get_db()
	cur = db.cursor()	
	cur.execute('select sid ,name,dailyScore,finalExamScore from student,studentCourse where cid=%s and sid=student.id', (cid))
	students=get_results(cur)
	return render_template('info/importScore.html', students=students,cid=cid)
	


@bp.route('/seeScore?cid=<cid>')
@login_required
def seeScore(cid):
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
