#!/usr/bin/python
#coding:utf-8

import xlsxwriter
from io import BytesIO
from ssms.db import get_db, get_results
def exportScoreList(cid):
	db = get_db()
	cur = db.cursor()
	sio = BytesIO()
	workbook = xlsxwriter.Workbook(sio, {'in_memory': True}) # xlwt.Workbook(encoding='ascii')   # 写到IO中
	cur.execute('select * from course where cid = %s' % cid)
	course = get_results(cur)[0]
	filename = '%s_%s_%s' % (course['cname'], course['courseyear'], course['courseterm'])
	worksheet = workbook.add_worksheet(name=filename)
	# worksheet.merge_range(0, 0, 0, 5, 'aaa')  # 合并单元格
	# worksheet.write(11, 2, '=SUM(1:10)')  # 增加公式
	# worksheet.set_default_row(35)  # 设置默认行高
	style1 = workbook.add_format({'font_size': '11', 'align': 'center', 'valign': 'vcenter', 'bold': True})   # 设置风格    'bg_color': '#34A0FF',
	style2 = workbook.add_format({'font_size': '11', 'align': 'center', 'valign': 'vcenter', 'bold': False})   # 'font_color': '#217346'
	worksheet.set_column('A:H', None, style2)
	worksheet.set_column(0, 7, 20)  # 设置列宽
	title = ['学号', '姓名', '学院','专业','平时成绩', '期末成绩', '最终成绩', '成绩状态']
	worksheet.write_row('A1', title, style1)
	cur.execute(
		'select sid, name, school, major, dailyScore, finalExamScore, score, studentExamStatus from student, studentCourse '
		'where sid = id and cid = %s',
		(cid)
	)
	scores = get_results(cur)
	i = 0
	for score in scores:
		data = [
			score['sid'],
			score['name'],
			score['school'],
			score['major'],
			score['dailyScore'],
			score['finalExamScore'],
			score['score'],
			score['studentExamStatus']
		]
		worksheet.write_row('A'+ str(i+2), data)
		i = i + 1

	workbook.close()
	sio.seek(0)		# 将byte流再从头读取，之前已经写到最后一个byte了
	resp = sio.getvalue()	# 通过getvalue函数读取IO流
	sio.close()	# 关闭IO流
	orderdata = [resp, filename.encode().decode('latin1')]	
	return orderdata
