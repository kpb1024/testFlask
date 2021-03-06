#!/usr/bin/python
#coding:utf-8

from flask import (
	Blueprint, flash, g, session, redirect, render_template, request, url_for, current_app, make_response
)
from flask.json import jsonify
from werkzeug.exceptions import abort
from ssms.auth import login_required
from ssms.db import get_db, get_results
from ssms.analysis import * 
from ssms.analysis2 import *
from ssms.utils import *

bp = Blueprint('info', __name__)

@bp.route('/', methods=('GET','POST'))
@login_required
def index():
	if session['auth'] == 2:
		id=session['id']
		db =get_db()
		cur = db.cursor()
		sql='select distinct course.cid,cname,dailyScoreRatioDesc,coursepoint,courseyear,courseterm,scoreType,scoreReviewStatus from course,teacher,studentCourse  where teacher.id=%s and teacher.id=course.tid and teacher.id=studentCourse.tid and studentCourse.cid=course.cid'% id
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
			return render_template('info/index3.html', courses=courses)
		cur.execute(sql)
		courses = get_results(cur)
		return render_template('info/index3.html', courses=courses)

	if session['auth'] == 1:
		id=session['id']
		db =get_db()
		cur = db.cursor()
		sql='select distinct course.cid,cname,dailyScoreRatioDesc,coursepoint,courseyear,courseterm,scoreType,scoreReviewStatus from course,teacher,studentCourse  where teacher.id=%s and teacher.id=course.tid and teacher.id=studentCourse.tid and studentCourse.cid=course.cid'% id
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
	sql = 'SELECT coursetype, cname, t.name, courseyear, courseterm, coursepoint, dailyScore, finalExamScore, score, gpa,`scoreReviewStatus` st, studentExamStatus '
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
		#cur.execute(sql)
		#courselist = get_results(cur)
		#return render_template('info/index.html', courses=courselist, scores=total_rank, cc=courseClass)
	cur.execute(sql)
	courselist = get_results(cur)
	if len(courselist) is 0:
		abort(404, "Student id {0} doesn't have Course score.".format(id))
	courseClass= {}
	for i in range(len(courseclass_gpa_rank(id))):
	    ctype=courseclass_gpa_rank(id)[i]['courseclass']
	    courseClass[ctype]=courseclass_gpa_rank(id)[i]
	sql = 'SELECT distinct c.cid, cname, t.name,courseyear,scoreReviewStatus FROM studentCourse sc JOIN course c JOIN teacher t where sc.tid = t.id and sc.cid = c.cid and '
	sql += 'sid = %s order by c.cid desc limit 3' % id
	cur.execute(sql)
	notices = get_results(cur)
	return render_template('info/index.html', courses=courselist, scores=total_rank,cc=courseClass,notices=notices)

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
		dailyScoreRatio = request.form['dailyScoreRatio']
		dailyScoreRatioDesc = request.form['dailyScoreRatioDesc']
		tid = g.user['id']
		db = get_db()
		cur = db.cursor()
		cur.execute(
			'INSERT INTO course(cname, courseterm, courseyear, coursepoint, coursetype, coursevolume, tid, dailyScoreRatio, dailyScoreRatioDesc, courseclass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
			(cname, courseterm, courseyear, coursepoint, coursetype, coursevolume, tid, dailyScoreRatio, dailyScoreRatioDesc, courseclass)
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
	if g.user['auth'] == 0:
		cur.execute(
			'select distinct * '
			'from proposal p join course c '
			'where p.cid = c.cid '
			'and p.sid = %s' % id
		)
	elif g.user['auth'] == 1:
		cur.execute(
			'select distinct * from proposal p join course c join student s '
			'where p.cid = c.cid and s.id = p.sid and p.cid in (select distinct cid from course where tid = %s)', id)
	else:
		cur.execute(
			'select distinct * from proposal p join course c join student s '
			'where p.cid = c.cid and s.id = p.sid'
		)
		
	proposals = get_results(cur)
	return render_template('info/showProposal.html', proposals = proposals)



@bp.route('/cancelProposal/<cid>')
@login_required
def cancelProposal(cid):
	db = get_db()
	cur = db.cursor()
	id = g.user['id']
	cur.execute('delete from proposal where cid = %s and sid = %s', (cid,id))
	db.commit()
	return redirect(url_for('info.showProposal'))

@bp.route('/reviewProposal/<cid>&<sid>')
@login_required
def reviewProposal(cid, sid):
	db = get_db()
	cur = db.cursor()
	if g.user['auth'] == 1:
		cur.execute('update proposal set is_checked_by_teacher = 1 where cid = %s and sid = %s', (cid,sid))
	elif g.user['auth'] == 2:
		cur.execute('update proposal set is_checked_by_dean = 1 where cid = %s and sid = %s', (cid,sid))
	db.commit()
	return redirect(url_for('info.showProposal'))



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
		courseyear.append(tg['courseyear'])
		courseterm.append(tg['courseterm'])
	return jsonify(term=courseterm, year=courseyear, gpa=gpa)

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
	cur.execute('select distinct course.cid,cname,coursetype,coursepoint,courseyear,courseterm,coursevolume,dailyScoreRatioDesc,scoreType,scoreReviewStatus from course,teacher,studentCourse  where teacher.id=%s and teacher.id=course.tid and teacher.id=studentCourse.tid and studentCourse.cid=course.cid',(id))
	courses = get_results(cur)
	return render_template('info/updateScore.html', courses=courses)
	

@bp.route('/importScore?cid=<cid>', methods=['GET', 'POST'])
@login_required
def importScore(cid):	
	id = session['id']
	db1=get_db()
	cur1=db1.cursor()
	cur1.execute('select distinct scoreType from studentCourse where cid=%s',(cid))
	type=get_results(cur1)
	db = get_db()
	cur = db.cursor()
	cur.execute('SELECT sid,name,school,major FROM student,studentCourse WHERE student.id=studentCourse.sid and cid = %s and tid=%s',(cid,id))
	students = get_results(cur)
	cur.execute('select  dailyScoreRatio from course where cid =%s',cid)
	per = get_results(cur)
	if type[0]['scoreType']=='百分制':
		if request.method=="POST":
			db = get_db()
			cur = db.cursor()
			cur.execute('select sid,name from studentCourse,student where cid=%s and sid=student.id',(cid))
			Students1=get_results(cur)
			for student in Students1:
				str1 = '%s%s' % (str(student['sid']),student['name']) #用+会坑，详见https://blog.csdn.net/zyz511919766/article/details/22072701
				StudentExamStatus = request.form[str1]
				if(StudentExamStatus == '正常'):#disabled之后请求不了dailyScore
					dailyScore = request.form[str(student['sid'])]
					finalExamScore = request.form[student['name']]
					cur.execute('select dailyScoreRatio from course where cid = %s' % cid)
					ratio = int(get_results(cur)[0]['dailyScoreRatio'])
					if(dailyScore==''):
						dailyScore=None
					else:
						dailyScore=int(dailyScore)
					if(finalExamScore==''):
						finalExamScore=None
					else:
						finalExamScore=int(finalExamScore)
						
					if(finalExamScore!=None and dailyScore!=None):
						score = (dailyScore*ratio + (100-ratio)*finalExamScore)/100
					else:
						score = None
					db.cursor().execute('update studentCourse set dailyScore=%s,finalExamScore=%s,StudentExamStatus=%s,score=%s where sid=%s and cid=%s',(dailyScore,finalExamScore,StudentExamStatus,score,student['sid'],cid))
				else:
					dailyScore=None
					finalExamScore=None
					score = None
					db.cursor().execute('update studentCourse set dailyScore=%s,finalExamScore=%s,StudentExamStatus=%s,score=%s where sid=%s and cid=%s',(dailyScore,finalExamScore,StudentExamStatus,score,student['sid'],cid))
			db.commit()
			return redirect(url_for('info.scoreMain', cid=cid))
		#cur.execute('SELECT sid,name,school,major FROM student,studentCourse WHERE student.id=studentCourse.sid and cid = %s and tid=%s',(cid,id))
		cur.execute('SELECT * FROM student,studentCourse WHERE student.id=studentCourse.sid and cid = %s and tid=%s',(cid,id))
		students = get_results(cur)
		return render_template('info/importScore.html', students=students, cid=cid,per=per)
	else:
		if request.method=="POST":
			db = get_db()
			cur = db.cursor()
			cur.execute('select sid,name from studentCourse,student where cid=%s and sid=student.id',(cid))
			Students1=get_results(cur)
			dailyScore=None
			finalExamScore=None
			for student in Students1:
				level=request.form['level']
				str1 = '%s%s' % (str(student['sid']),student['name']) #用+会坑，详见https://blog.csdn.net/zyz511919766/article/details/22072701
				StudentExamStatus = request.form['status']
				if level=='优秀':
					score=95
				elif level=='良好':
					score=85
				elif level=='一般':
					score=75
				elif level=='合格':
					score=65
				elif level=='不合格':
					score=55
				else:
					score=None	#空键处理
				db.cursor().execute('update studentCourse set dailyScore=%s,finalExamScore=%s,score=%s,StudentExamStatus=%s where sid=%s and cid=%s',(dailyScore,finalExamScore,score,StudentExamStatus,student['sid'],cid))
				db.commit()
			return redirect(url_for('info.scoreMain', cid=cid))
		return render_template('info/importScore0.html', students=students, cid=cid,per=per)#需要等级制页面吗
	


@bp.route('/seeScore?cid=<cid>')
@login_required
def seeScore(cid):
	tid = session['id']
	db = get_db()
	cur1 = db.cursor()
	cur1.execute('select sid ,name,dailyScore,finalExamScore,score,scoreReviewStatus from student,studentCourse where cid=%s and sid=student.id',(cid))
	scores=get_results(cur1)	
	db.commit()
	return render_template('info/seeScore.html', scores=scores)

@bp.route('/setPercent?cid=<cid>', methods=['GET', 'POST'])
@login_required
def setPercent(cid):
	tid = session['id']
	db = get_db()
	cur = db.cursor()
	cur.execute('SELECT sid,name,school,major FROM student,studentCourse WHERE student.id=studentCourse.sid and cid = %s and tid=%s',(cid,tid))
	students = get_results(cur)
	if request.method == 'POST':
		tid = session['id']
		dailyScoreRatio=request.form['dailyScoreRatio']
		a=100-int(dailyScoreRatio)
		dailyScoreRatioDesc="平时成绩("+dailyScoreRatio+"%)，期末成绩("+str(a)+"%)"
		db = get_db()
		db.cursor().execute('update course set dailyScoreRatio=%s,dailyScoreRatioDesc=%s where cid=%s',(dailyScoreRatio,dailyScoreRatioDesc,cid))
		db.commit()
		return redirect(url_for('info.importScore', cid=cid))
	db1 = get_db()
	cur1=db1.cursor()
	cur1.execute('select distinct dailyScoreRatio from course where cid=%s',(cid))
	per=get_results(cur1)
	db1.commit()
	return redirect(url_for('info.importScore', cid=cid))	

	
@bp.route('/review', methods=['GET', 'POST'])
@login_required
def review():
	db = get_db()
	cur = db.cursor()
	cur.execute('select cid,cname,coursetype,coursepoint,courseyear,courseterm,coursevolume,name from course,teacher')
	courses = get_results(cur)
	return render_template('info/review.html', courses=courses)


@bp.route('/reviewGrade?cid=<cid>', methods=['GET', 'POST'])
@login_required
def reviewGrade(cid):
	if request.method == 'POST':
		radio=request.form['radio']
		if radio=='√':
			db1 = get_db()	
			cur1 = db1.cursor()
			cur1.execute('update studentCourse set scoreReviewStatus=%s where cid=%s',('审核完毕',cid))
			db1.commit()
			cur1.execute('select email from user where id in (select sid from studentCourse where cid = %s)', (cid))
			emails = get_results(cur1)
			email_list = []
			for email in emails:
				if email['email'] is not '':
					email_list.append(email['email'])
			cur1.execute(
				'select cname from course where cid = %s',
				(cid))
			mesg = '同学你所选的课程——{}的课程成绩已经审核完毕，请查看'
			send_email(mesg.format(get_results(cur1)[0]['cname']), email_list)
		else:
			feedback=request.form['feedback']
			db2 = get_db()	
			cur2 = db2.cursor()
			cur2.execute('update studentCourse set scoreReviewStatus=%s where cid=%s',(feedback,cid))
	db = get_db()
	cur = db.cursor()
	cur.execute('select sid ,name,dailyScore,finalExamScore,score,scoreReviewStatus from student,studentCourse where cid=%s and sid=student.id',(cid))
	scores=get_results(cur)
	return render_template('info/reviewGrade.html', scores=scores)


@bp.route('/courseAnalysis?cid=<cid>',methods=('GET','POST'))
@login_required
def courseAnalysis(cid):
	db = get_db()
	cur = db.cursor()
	fail = course_fail(cid)
	count = course_count2(cid)
	cur.execute(
	        'SELECT id, name, dailyScore, finalExamScore, score FROM studentCourse JOIN student ON id = sid WHERE cid = %s',
	        (cid)
	)
	students = get_results(cur)
	
	cur.execute(
	        'SELECT cid,cname FROM course WHERE cid = %s',
	        (cid)
	)
	course = get_results(cur)
	
	cur.execute(
	        'SELECT avg(score), max(score), min(score) FROM studentCourse JOIN student ON id = sid WHERE cid = %s',
	        (cid)
	)
	score = get_results(cur)
	
	db.commit()
	return render_template('info/teacher2.html', students = students,course = course, score=score, fail=fail, count=count)

@bp.route('/teacher2_graph/<cid>', methods=('GET', 'POST'))
@login_required
def teacher2_graph(cid):
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
	
@bp.route('/scoreMain?cid=<cid>', methods=('GET','POST'))
@login_required
def scoreMain(cid):
	id = session['id']
	db = get_db()
	cur = db.cursor()
	cur.execute('SELECT sid,name,school,major,dailyScore,finalExamScore,score,studentExamStatus FROM student,studentCourse WHERE student.id=studentCourse.sid and cid = %s and tid=%s',(cid,id))
	courses = get_results(cur)
	cur.execute('select courseyear,courseterm,cname,dailyScoreRatioDesc from course where cid = %s',(cid))
	info = get_results(cur)
	return render_template('info/scoreMain.html', courses=courses, cid=cid,info=info)

@bp.route('/getExcelByCid/<cid>')
def getExcelByCid(cid):
	respdata = exportScoreList(cid)
	resp = make_response(respdata[0])
	resp.headers["Content-Disposition"] = "attachment; filename={}.xlsx".format(respdata[1])
	resp.headers['Content-Type'] = 'application/x-xlsx'
	return resp

@bp.route('/selectAna', methods=('GET', 'POST'))
@login_required		
def selectAna():
	courses = {}
	sid = session['id']
	db = get_db()
	cur = db.cursor()
	cc=""
	cy=""
	ccd=""
	cyd=""
	if request.method == 'POST':
		courseclass = request.form.getlist('coursetype')
		courseyear = request.form.getlist('courseyear')
		cc="' or ".join(("courseclass = '" + str(n) for n in courseclass))
		cy = "' or ".join(("courseyear = '" + str(n) for n in courseyear))
		cc=cc+"'"
		cy=cy+"'"
		query= 'CREATE TEMPORARY TABLE scores select sid,ROUND(sum(sc)/sum(coursepoint),2) as avggpa from (select gpa*coursepoint sc, coursepoint,sid from course, studentCourse where course.cid = studentCourse.cid and (' +cc+') and ('+cy+')) as s GROUP BY sid '
		cur.execute(query)
		query1= 'CREATE TEMPORARY TABLE scores1 select sid,ROUND(sum(sc)/sum(coursepoint),2) as avggpa from (select gpa*coursepoint sc, coursepoint,sid from course, studentCourse where course.cid = studentCourse.cid and (' +cc+') and ('+cy+')) as s GROUP BY sid '
		cur.execute(query1)
		
		query2='SELECT avggpa, FIND_IN_SET( avggpa, (SELECT GROUP_CONCAT( avggpa ORDER BY avggpa DESC ) FROM scores ))  as rk FROM scores1 where sid = %s'
		cur.execute(query2,sid)
		courses = get_results(cur)
	
		for i in courseclass:
			if i == 'gx':
				ccd = ccd +" 公选 "
			elif i == 'gb':
				ccd = ccd +" 公必 "
			elif i == 'zb':
				ccd = ccd +" 专必 "
			elif i == 'zx':
				ccd = ccd +" 专选 "
		for i in courseyear:
			if i == '2018':
				cyd = cyd +" 2018 "
			elif i == '2019':
				cyd = cyd +" 2019 "
			elif i == '2017':
				cyd = cyd +" 2017 "
				
	return render_template('info/selectAna.html', courses=courses,cc=ccd,cy=cyd)
