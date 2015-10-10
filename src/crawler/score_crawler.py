'''
Created on 2015年9月1日

@author: wan
'''
from bs4 import BeautifulSoup as Soup
from spyne.model.complex import ComplexModel
from urllib import request, parse
from crawler import CHARSET
from spyne import Unicode


class Score(ComplexModel):
    def __init__(self, course_id, course_name, type1, type2, credit, grade_point, normal_performance, midterm_exam_score,final_exam_score,
                 experiment_score, score, minor_mark, make_up_exam_achievement, rebuild_achievement, academy_name, remark, rebuild_mark):
        self.course_id = course_id
        self.course_name = course_name
        self.type1 = type1
        self.type2 = type2
        self.credit = credit
        self.grade_point = grade_point
        self.normal_performance = normal_performance
        self.midterm_exam_score = midterm_exam_score
        self.final_exam_score = final_exam_score
        self.experiment_score = experiment_score
        self.score = score
        self.minor_mark = minor_mark
        self.make_up_exam_achievement = make_up_exam_achievement
        self.rebuild_achievement = rebuild_achievement
        self.academy_name = academy_name
        self.remark = remark
        self.rebuild_mark = rebuild_mark

    course_id = Unicode
    course_name = Unicode
    type1 = Unicode
    type2 = Unicode
    credit = Unicode
    grade_point = Unicode
    normal_performance = Unicode
    midterm_exam_score = Unicode
    final_exam_score = Unicode
    experiment_score = Unicode
    score = Unicode
    minor_mark = Unicode
    make_up_exam_achievement = Unicode
    rebuild_achievement = Unicode
    academy_name = Unicode
    remark = Unicode
    rebuild_mark = Unicode

def crawl(cookie, student_number, year, term):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    url = 'http://jw.gdufs.edu.cn/xscj_gc.aspx?student_number=%s' % student_number
    soup = Soup(opener.open(url), from_encoding=CHARSET)
    view_state = soup.find('input', {'name':'__VIEWSTATE'})['value']
    post_data = {'BUTTON1':'按学期查询', 'ddlXN':year, 'ddlXQ':term, '__VIEWSTATE':view_state}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request(url, post_data)
    soup = Soup(opener.open(req), from_encoding=CHARSET)
    table = soup.table
    table.tr.decompose()
    score_list = []
    for item in table.find_all('tr'):
        course_id = item.contents[3].text
        course_name = item.contents[4].text
        type1 = item.contents[5].text
        type2 = item.contents[6].text
        credit = item.contents[7].text
        grade_point = item.contents[8].text
        normal_performance = item.contents[9].text
        midterm_exam_score = item.contents[10].text
        final_exam_score = item.contents[11].text
        experiment_score = item.contents[12].text
        score = item.contents[13].text
        minor_mark = item.contents[14].text
        make_up_exam_achievement = item.contents[15].text
        rebuild_achievement = item.contents[16].text
        academy_name = item.contents[17].text
        remark = item.contents[18].text
        rebuild_mark = item.contents[19].text
        score_list.append(Score(course_id, course_name, type1, type2, credit, grade_point, normal_performance, midterm_exam_score,final_exam_score,
                 experiment_score, score, minor_mark, make_up_exam_achievement, rebuild_achievement, academy_name, remark, rebuild_mark))
    return score_list

if __name__ == '__main__':
    from crawler import COOKIE
    from util import cookie_from_str
    cookie = cookie_from_str(COOKIE)
    for item in crawl(cookie, '20131003502', '2014-2015', '1'):
        print(item)