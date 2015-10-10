'''
Created on 2015年8月18日

@author: wan
'''
from bs4 import BeautifulSoup as Soup
import re
from spyne import Unicode, Integer
from spyne.model.complex import ComplexModel
from urllib import request, parse

from crawler import CHARSET


__DATE_DICT = {'一':0, '二':1, '三':2, '四':3, '五':4, '六':5, '日':6}
class Course(ComplexModel):
    course_name = Unicode
    teacher_name = Unicode
    place = Unicode
    start_time = Integer
    numb = Integer
    def __init__(self, course_name, teacher_name, place, start_time, numb):
        self.course_name, self.teacher_name, self.place, self.start_time, self.numb =\
        course_name, teacher_name, place, start_time, numb
def crawl(cookie, student_number, year, term):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    url = 'http://jw.gdufs.edu.cn/xskbcx.aspx?student_number=%s' % student_number
    soup = Soup(opener.open(url), from_encoding=CHARSET)
    view_state = soup.find('input', {'name':'__VIEWSTATE'})['value']
    table = soup.table
    selected_list = table.find_all('option', {'selected':True})
    if len(selected_list) == 2 and year == selected_list[0]['value'] and term == selected_list[1]['value']:
        table = soup.find_all('table')[1]
    else:
        post_data = {'__EVENTTARGET':'', 'xnd':year, 'xqd':term, '__VIEWSTATE':view_state}
        post_data = parse.urlencode(post_data).encode(CHARSET)
        req = request.Request(url, post_data)
        soup = Soup(opener.open(req), from_encoding=CHARSET)
        table = soup.find_all('table')[1]
    course_table = [[], [], [], [], [], [], []]
    table.tr.decompose()
    for td in table.find_all('td', {'align':'Center'}):
        if re.match('\\s+', td.text):
            continue
        content = [item for item in re.split('<.+?>', str(td)) if item]
        course_name = content[0]
        teacher_name = content[2]
        place = content[3]
        matcher = re.search('周(.*)第(.*)节', content[1])
        t = matcher.group(2).split(',')
        start_time = t[0]
        numb = len(t)
        course = Course(course_name, teacher_name, place, start_time, numb)
        course_table[__DATE_DICT[matcher.group(1)]].append(course)
    return course_table

if __name__ == '__main__':
    from crawler import COOKIE
    from util import cookie_from_str
    cookie = cookie_from_str(COOKIE)
    print(crawl(cookie, '20131003502', '2015-2016', '1'))