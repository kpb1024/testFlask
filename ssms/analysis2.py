#!/usr/bin/python
#coding:utf-8
from ssms.db import get_db, get_results

	
# 指定课程总人数 表
# tested
def course_count2(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select count(*) count from studentCourse JOIN student ON id = sid where cid = %s', (cid))
	course_count = get_results(cur)
	return course_count
	

#  成绩分布	图
# tested
def course_score(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute(
		'select count(*) 小于60 from studentCourse JOIN student ON id = sid where cid = %s and score < 60',
		(cid))
	score_distribution = get_results(cur)
	cur.execute(
		'select count(*) 60至70 from studentCourse JOIN student ON id = sid where cid = %s and score >= 60 and score < 70',
		(cid))
	score_distribution.extend(get_results(cur))
	cur.execute(
		'select count(*) 70至80 from studentCourse JOIN student ON id = sid where cid = %s and score >= 70 and score < 80',
		(cid))
	score_distribution.extend(get_results(cur))
	cur.execute(
		'select count(*) 80至90 from studentCourse JOIN student ON id = sid where cid = %s and score >= 80 and score < 90',
		(cid))
	score_distribution.extend(get_results(cur))
	cur.execute(
		'select count(*) 90至100 from studentCourse JOIN student ON id = sid where cid = %s and score >= 90',
		(cid))
	score_distribution.extend(get_results(cur))
	return score_distribution

def course_fail(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute(
		'select round((count(score<60 or null)) /count(score) *100 , 2) fail from studentCourse JOIN student ON id = sid where cid = %s',(cid)
	)
	course_fail = get_results(cur)
	return course_fail