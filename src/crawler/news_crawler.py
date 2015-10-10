'''
Created on 2015年9月1日

@author: wan
'''
from spyne.model.complex import ComplexModel
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
from crawler import CHARSET
import re
from spyne import Unicode


NEWS = 'gwxw'
ANNOUNCEMENT = 'tzgg'

class News(ComplexModel):
    date = Unicode
    title = Unicode
    url = Unicode
    def __init__(self, date, title, url):
        self.date, self.title, self.url = date, title, url

def crawl(aim, page=1):
    if aim not in [NEWS, ANNOUNCEMENT]:
        return []
    url = 'http://www.gdufs.edu.cn/%s.htm' % aim
    soup = Soup(urlopen(url), from_encoding=CHARSET)
    if page != 1:
        try:
            td = soup.find('td', id=re.compile('fanye.+'))
            max_page = eval(re.search('\\d+/(\\d+)', td.text).group(1)) + 1
        except:
            max_page = 1
        if max_page <= page:
            return []
        else:
            url = 'http://www.gdufs.edu.cn/%s/%u.htm' % (aim, max_page - page)
        soup = Soup(urlopen(url), from_encoding=CHARSET)
    news_list = []
    for li in soup.find('div', {'class':'m_content'}).find_all('li'):
        date = li.contents[1].text
        title = li.contents[3].text
        url = 'http://www.gdufs.edu.cn/%s' % li.contents[3].a['href'].replace('../', '')
        news_list.append(News(date, title, url))
    return news_list

if __name__ == '__main__':
    for item in crawl(NEWS, 1):
        print(item)