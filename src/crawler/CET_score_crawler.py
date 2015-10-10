'''
Created on 2015年8月18日

@author: wan
'''
from bs4 import BeautifulSoup as Soup
from spyne import Unicode
from spyne.model.complex import ComplexModel
from urllib import request
from crawler import CHARSET


class CETScore(ComplexModel):
    year = Unicode
    term = Unicode
    examination_name = Unicode
    examinee_number = Unicode
    date = Unicode
    score = Unicode
    listening_score = Unicode
    reading_score = Unicode
    writing_score = Unicode
    comprehensive_score = Unicode
    def __init__(self, year, term, examination_name, examinee_number, date, score,
                 listening_score, reading_score, writing_score, comprehensive_score):
        (self.year, self.term, self.examination_name, self.examinee_number, self.date, self.score, self.listening_score,
         self.reading_score, self.writing_score, self.comprehensive_score)\
         = (year, term, examination_name, examinee_number, date, score, listening_score, reading_score, writing_score,
            comprehensive_score)
def crawl(cookie, student_number):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    soup = Soup(opener.open('http://jw.gdufs.edu.cn/xsdjkscx.aspx?student_number=%s' % student_number), from_encoding=CHARSET)
    table = soup.table
    del table.attrs
    table.tr.decompose()
    CET_score_list = []
    for item in table.find_all('tr'):
        CET_score_list.append(CETScore(item.contents[1].text, item.contents[2].text, item.contents[3].text,
                                        item.contents[4].text, item.contents[5].text, item.contents[6].text, item.contents[7].text,
                                        item.contents[8].text, item.contents[9].text, item.contents[10].text))
    return CET_score_list

if __name__ == '__main__':
    from crawler import COOKIE
    from util import cookie_from_str
    cookie = cookie_from_str(COOKIE)
    print(crawl(cookie, '20131003502'))