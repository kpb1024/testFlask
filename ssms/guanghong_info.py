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
		'select courseTerm, avg(score), max(score), min(score) from Performances, Courses where Performances.courseNo=Courses.courseNo'
		'and studentNo=? group by courseTerm', (sid,)).fetchall()
		
	if analysis is None:
		abort(404, "Student id{0} doesn't have any score.".format(sid))
		
	return jsonify(term = [x[0] for x in analysis], avg = [x[1] for x in analysis], max = [x[2] for x in analysis], min = [x[3] for x in analysis])
