#!/usr/bin/python
#coding:utf-8
from ssms.db import get_db, get_results
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# 1. 综合排名
# tested
def avg_coursetype(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select avg(gpa) gpa, coursetype, sum(coursepoint) coursepoint from course, studentCourse where sid = %s and course.cid = studentCourse.cid group by coursetype', (sid))
	avg_coursetype = get_results(cur)
	return avg_coursetype
	
# tested	
def total_point(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select sum(coursepoint) totalpoint from course, studentCourse where sid = %s and course.cid = studentCourse.cid', (sid))
	total_point = get_results(cur)
	point = total_point
	return point


# tested	
def total_avg_gpa(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select sum(sc)/sum(coursepoint) avggpa from (select gpa*coursepoint sc, coursepoint from course, studentCourse where sid = %s and course.cid = studentCourse.cid) as s', (sid))
	total_avg_gpa = get_results(cur)
	return total_avg_gpa

# 综合绩点变化趋势
# tested
def term_avg_gpa(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select ANY_VALUE(sum(gpa*coursepoint)/sum( coursepoint)) gp,courseyear,courseterm from course, studentCourse where sid = %s and course.cid = studentCourse.cid group by courseyear,courseterm', (sid))
	term_avg_gpa = get_results(cur)
	return term_avg_gpa

# 公选公必
# tested
def courseclass_gpa_rank(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select ANY_VALUE(sum(gpa*coursepoint)/sum( coursepoint)) gp,  ANY_VALUE(sum(coursepoint)) ttpoint, courseclass from course, studentCourse where sid = %s and course.cid = studentCourse.cid group by courseclass', (sid))
	courseclass_gpa_rank = get_results(cur)
	return courseclass_gpa_rank

# 2. 综合排名变化趋势
# tested
def courseterm_rank(sid):
	db = get_db()
	cur = db.cursor()
	sql = '''
	select totalrank, courseterm from (
	select sid, courseterm, row_number() over(PARTITION by courseterm order by avggpa desc) totalrank from (
	select sum(sc)/sum(coursepoint) avggpa, courseterm, sid from (
	select gpa*coursepoint sc, coursepoint, courseterm, sid from course, studentCourse where course.cid = studentCourse.cid) as s group by courseterm, sid) as s) as s where sid = %s
	'''
	cur.execute(sql, (sid))
	courseterm_rank = get_results(cur)
	return courseterm_rank
	
# 3. 个人成绩分布图
# tested
def score_distribution(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select count(*) 小于60 from course, studentCourse where sid = %s and course.cid = studentCourse.cid and score < 60', (sid))
	score_distribution = get_results(cur)
	cur.execute('select count(*) 60至70 from course, studentCourse where sid = %s and course.cid = studentCourse.cid and score >= 60 and score < 70', (sid))
	score_distribution.extend(get_results(cur))
	cur.execute('select count(*) 70至80 from course, studentCourse where sid = %s and course.cid = studentCourse.cid and score >= 70 and score < 80', (sid))
	score_distribution.extend(get_results(cur))
	cur.execute('select count(*) 80至90 from course, studentCourse where sid = %s and course.cid = studentCourse.cid and score >= 80 and score < 90', (sid))
	score_distribution.extend(get_results(cur))
	cur.execute('select count(*) 90至100 from course, studentCourse where sid = %s and course.cid = studentCourse.cid and score >= 90', (sid))
	score_distribution.extend(get_results(cur))
	return score_distribution
	
# 4. 优势学科
# tested	
def top_subject(sid):
	db = get_db()
	cur = db.cursor()
	i = cur.execute('select score, gpa, course.cid cid, course.cname cname from course, studentCourse where sid = %s and course.cid = studentCourse.cid and score >= 90 order by gpa desc limit 3', (sid))
	if i != 0:
		top_subject = get_results(cur)
	else:
		cur.execute('select score, gpa, course.cid cid, course.cname cname from course, studentCourse where sid = %s and course.cid = studentCourse.cid order by gpa desc limit 1', (sid))
		top_subject = get_results(cur)
	return top_subject

# 5. 劣势学科
# tested
def worst_subject(sid):
	db = get_db()
	cur = db.cursor()
	i = cur.execute('select score, gpa, course.cid cid, course.cname cname from course, studentCourse where sid = %s and course.cid = studentCourse.cid and score <= 70 order by gpa limit 3', (sid))
	if i != 0:
		worse_subject = get_results(cur)
	else:
		cur.execute('select score, gpa, course.cid cid, course.cname cname from course, studentCourse where sid = %s and course.cid = studentCourse.cid order by gpa limit 1', (sid))
		worse_subject = get_results(cur)
	return worse_subject
	
# 指定课程平均分 表
# tested
def course_avg(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select avg(score) avg from studentCourse where cid = %s', (cid))
	course_avg = get_results(cur)
	return course_avg
	
# 指定课程总人数 表
# tested
def course_count(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select count(*) count from studentCourse where cid = %s', (cid))
	course_count = get_results(cur)
	return course_count
	
# 指定课程学生排名 表
# tested
def student_rank(cid, sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select rnk from (select sid, rank() over(order by score desc) rnk from (select * from studentCourse where cid = %s) as s) as c where sid=%s', (cid, sid))
	student_rank = get_results(cur)
	return student_rank

# 6. 成绩分布	图
# tested
def course_score(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute(
		'select count(*) 小于60 from studentCourse where cid = %s and score < 60',
		(cid))
	score_distribution = get_results(cur)
	cur.execute(
		'select count(*) 60至70 from studentCourse where cid = %s and score >= 60 and score < 70',
		(cid))
	score_distribution.extend(get_results(cur))
	cur.execute(
		'select count(*) 70至80 from studentCourse where cid = %s and score >= 70 and score < 80',
		(cid))
	score_distribution.extend(get_results(cur))
	cur.execute(
		'select count(*) 80至90 from studentCourse where cid = %s and score >= 80 and score < 90',
		(cid))
	score_distribution.extend(get_results(cur))
	cur.execute(
		'select count(*) 90至100 from studentCourse where cid = %s and score >= 90',
		(cid))
	score_distribution.extend(get_results(cur))
	return score_distribution

# 6. 成绩分布	表
# tested
def course_info(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select avg(score) avg, max(score) max, count(score > 85 or null)/ count(*) good from studentCourse where cid = %s', (cid))
	course_info = get_results(cur)
	return course_info

#6. 获得所有参加过的课程

def course_involve(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select course.cid, cname from course, studentCourse where sid = %s and studentCourse.cid = course.cid', (sid))
	course_involve = get_results(cur)
	return course_involve

def send_email(msg, to):
	# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
	message = MIMEText(msg, 'plain', 'utf-8')
	#message['from'] = '757139408@qq.com'
	#password = "ythmxdzhmcxhbahi"
	message['from'] = 'kangpeibang@qq.com'
	#password = "hmceqjhelsxbcbbf"
	password = "qynkjhmxppyrcajj"

	message['subject'] = Header(u'教务系统消息', 'utf-8').encode()
	smtp_server = "smtp.qq.com"
	#smtp_server = '127.0.0.1'
	server = smtplib.SMTP_SSL(smtp_server,465)  # SMTP协议默认端口是25
	# 打印出和SMTP服务器交互的所有信息。
	# server.set_debuglevel(1)
	# 登录SMTP服务器
	server.login(message['from'], password)
	# 发邮件，由于可以一次发给多个人，所以传入一个list;
	# 邮件正文是一个str，as_string()把MIMEText对象变成str。
	server.sendmail(message['from'], to, message.as_string())
	server.quit()

