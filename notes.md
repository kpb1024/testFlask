# From 广泓
echartsÊµÏÖ£º
Ñ§Éú£º
±ä»¯Ç÷ÊÆ·ÖÎö
select courseTerm, avg(score), max(score), min(score) from Performances, Courses where Performances.courseNo=Courses.courseNo
and studentNo={given} group by courseTerm
ÓÅÁÓÊÆ·ÖÎö data
select studentNo, courseName, score from Performances, Courses where Performances.courseNo=Courses.courseNo and studentNo={given}
and courseTerm={given}
°´ÕÕÑ§Äê£¬Ñ§¿ÆÀà±ð½øÐÐ³É¼¨Õ¹Ê¾ data
select courseName, score, GPA, render, entryStatus from Performances, Courses where studentNo={given}
and Performances.courseNo in (select courseNo from Courses where courseCate={given} and courseTerm={given}) and Performances.courseNo=Courses.courseNo
ÀÏÊ¦£º
¸÷¿ÆÆ½¾ù·Ö£¬×î¸ß·Ö£¬ÓÅÐãÂÊ
select courseNo, avg(score), max(score), count(if(score >= 80, true, null))/count(score) from Performances, Courses where teacherNo={given} 
and Courses.courseNo=Performances.courseNo group by courseNo
¸÷¿Æ³É¼¨·Ö²¼

Ç°¶ËÌá½»±íµ¥-ºó¶Ë²éÑ¯Êý¾Ý¿â-ºó¶ËÉú³Éjson-Ç°¶Ë»ñµÃjson-Ç°¶ËÉú³É±í¸ñÁ÷³Ì£º
Ç°¶ËÌá½»±íµ¥²¢»ñµÃjson£º<el-form> @clickµ÷ÓÃfunction ÅÐ¶ÏÊÇ·ñÎª¿Õ
let url = Flask.url_for("selectedScore");
                axios.post(url, {
                    term: self.form.term //Ìá½»²ÎÊý
	    cate: self.form.cate
                })then(function(response) {
		self.tableData = response.data.results;}); //»ñµÃÊý¾Ý
ºó¶Ë²éÑ¯Êý¾Ý¿â²¢Éú³Éjson:
Ê¹ÓÃ term = request.json.get('term')»ñµÃÊý¾Ý
return jsonify({'results': results})
(results=[] results.append({'name':'', 'id':''}))

Ç°¶ËÉú³É±í¸ñ£º
:data='tableData'
