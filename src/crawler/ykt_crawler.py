'''
Created on 2015年9月2日

@author: wan
'''
from spyne import Integer, Unicode, Float
from spyne.model.complex import ComplexModel
from bs4 import BeautifulSoup as Soup
from urllib import request, parse
from crawler import CHARSET
import re


STATE_DICT = {'正常':0, '冻结':1}
YKT_TRY_URL = 'http://ykt.gdufs.edu.cn/gdufsPortalHome.action'
YKT_INFORMATION_URL = 'http://ykt.gdufs.edu.cn/accountcardUser.action'
YKT_ACCOUNT_URL = 'http://ykt.gdufs.edu.cn/accounthisTrjn.action'
YKT_TODAY_ACCOUNT_URL = 'http://ykt.gdufs.edu.cn/accounttodatTrjnObject.action'
YKT_HISTORY_ACCOUNT_URL = 'http://ykt.gdufs.edu.cn/accountconsubBrows.action'
ACTION_DICT = {'查询全部':'all', '存款':'13', '取款':'14', '消费':'15', '转帐':'16', '补助':'17', '扣款':'18',
               '电子账户交费':'76', '电子账户退费':'77', '电子账户存款':'90', '电子账户取款':'91', '电子账户转出':'92',
               '电子账户转入':'93', '电子账户消费':'94', '电子账户银行转帐':'95', '电子账户补助':'96', '电子账户扣款':'97',
               '电子账户商户退款':'98'}
def _sub_system_name_make_up(name):
    name = name.replace('食..', '食堂')
    name = name.replace('凉..', '凉茶坊')
    name = name.replace('交..', '交流中心')
    name = name.replace('..', '')
    return name
YKT_RECHARGE_URL = 'http://ykt.gdufs.edu.cn/gzwywmYhzzIndex.action'
YKT_RECHARGE_URL2 = 'http://ykt.gdufs.edu.cn/gzwywmYhzz.action'
YKT_MODIFY_PASSWORD_URL = 'http://ykt.gdufs.edu.cn/accountcpwd.action'
YKT_MODIFY_PASSWORD_URL2 = 'http://ykt.gdufs.edu.cn/accountDocpwd.action'
YKT_PASSWORD_PHOTO_URL = 'http://ykt.gdufs.edu.cn/getpasswdPhoto.action'
YKT_REPORT_LOSS_URL = 'http://ykt.gdufs.edu.cn/accountloss.action'
YKT_REPORT_LOSS_URL2 = 'http://ykt.gdufs.edu.cn/accountDoLoss.action'

class YKTInformation(ComplexModel):
    state = Integer
    balance = Float
    transition_balance = Float
    def __init__(self, state, balance, transition_balance):
        self.state = state
        self.balance = balance
        self.transition_balance = transition_balance

class Account(ComplexModel):
    def __init__(self, time, transaction_type, sub_system_name, electronic_account, trading_volume, balance, state):
        self.time = time
        self.transaction_type = transaction_type
        self.sub_system_name = sub_system_name
        self.electronic_account = electronic_account
        self.trading_volume = trading_volume
        self.balance = balance
        self.state = state
    time = Unicode
    transaction_type = Unicode
    sub_system_name = Unicode
    electronic_account= Unicode
    trading_volume = Float
    balance = Float
    state = Unicode

def _match_from_tr(account_list, trs):
    for tr in trs:
        tds = tr.find_all('td')
        time = tds[0].text
        transaction_type = tds[1].text
        sub_system_name = _sub_system_name_make_up(tds[2].text)
        electronic_account= tds[3].text
        trading_volume = eval(tds[4].text)
        balance = eval(tds[5].text)
        state = tds[7].text
        account_list.append(Account(time, transaction_type, sub_system_name, electronic_account, trading_volume, balance, state))
        
def crawl_today_account(cookie, account=None, action=None):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    opener.open(YKT_TRY_URL)
    if not account or not action:
        soup = Soup(opener.open(YKT_ACCOUNT_URL), from_encoding=CHARSET)
        selects = soup.find_all('select')
        if not account:
            account = selects[0].option['value']
        if not action:
            action = selects[1].option['value']
    post_data = {'account':account, 'inputObject':action, 'Submit':'+%C8%B7+%B6%A8+'}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request(YKT_TODAY_ACCOUNT_URL, post_data)
    soup = Soup(opener.open(req), from_encoding=CHARSET)
    table = soup.find('table', id='tables')
    trs = table.find_all('tr')
    pages = eval(re.search('共(\\d+)页', trs[-1].text).group(1))
    if pages == 0:
        return []
    account_list = []
    _match_from_tr(account_list, trs[1:-1])
    page = 1
    while True:
        page += 1
        if page > pages:
            break
        post_data = {'account':account, 'inputObject':action, 'pageVo.pageNum':page}
        post_data = parse.urlencode(post_data).encode(CHARSET)
        req = request.Request(YKT_TODAY_ACCOUNT_URL, post_data)
        soup = Soup(opener.open(req), from_encoding=CHARSET)
        table = soup.find('table', id='tables')
        trs = table.find_all('tr')
        _match_from_tr(account_list, trs[1:-1])
    return account_list
    
def crawl_ykt_information(cookie):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    opener.open(YKT_TRY_URL)
    soup = Soup(opener.open(YKT_INFORMATION_URL), from_encoding=CHARSET)
    table = soup.table.table
    state = STATE_DICT[table.find('div', text='卡  状  态：').findNext('td').text.strip()]
    balance_str = table.find('div', text='余    额：').findNext('td').text.strip()
    balance_list = re.findall('(\\d+\.\\d+)元', balance_str)
    balance = eval(balance_list[0])
    transition_balance = eval(balance_list[1]) + eval(balance_list[2])
    return YKTInformation(state, balance, transition_balance)

def crawl_history_account(cookie, start_day, end_day, account=None, action=None):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    opener.open(YKT_TRY_URL)
    soup = Soup(opener.open(YKT_ACCOUNT_URL), from_encoding=CHARSET)
    url = 'http://ykt.gdufs.edu.cn%s' % soup.form['action']
    if not account or not action:
        selects = soup.find_all('select')
        if not account:
            account = selects[0].option['value']
        if not action:
            action = selects[1].option['value']
    post_data = {'account':account, 'inputObject':action, 'Submit':'+%C8%B7+%B6%A8+'}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request(url, post_data)
    soup = Soup(opener.open(req), from_encoding=CHARSET)
    url = 'http://ykt.gdufs.edu.cn%s' % soup.form['action']
    post_data = {'inputStartDate':start_day, 'inputEndDate':end_day}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request(url, post_data)
    soup = Soup(opener.open(req), from_encoding=CHARSET)
    url = 'http://ykt.gdufs.edu.cn/accounthisTrjn.action%s' % soup.form['action']
    soup = Soup(opener.open(url), from_encoding=CHARSET)
    table = soup.find('table', id='tables')
    trs = table.find_all('tr')
    pages = eval(re.search('共(\\d+)页', trs[-1].text).group(1))
    if pages == 0:
        return []
    account_list = []
    _match_from_tr(account_list, trs[1:-1])
    page = 1
    while True:
        page += 1
        if page > pages:
            break
        post_data = {'inputStartDate':start_day, 'inputEndDate':end_day, 'pageNum':page}
        post_data = parse.urlencode(post_data).encode(CHARSET)
        req = request.Request(YKT_HISTORY_ACCOUNT_URL, post_data)
        soup = Soup(opener.open(req), from_encoding=CHARSET)
        table = soup.find('table', id='tables')
        trs = table.find_all('tr')
        _match_from_tr(account_list, trs[1:-1])
    return account_list

def recharge(cookie, money, password):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    opener.open(YKT_TRY_URL)
    soup = Soup(opener.open(YKT_RECHARGE_URL), from_encoding=CHARSET)
    form = soup.form
    post_data = {'area':str(money), 'newpasswd':password}
    post_data['bankAcc'] = form.find('input', {'name':'bankAcc'})['value']
    post_data['account'] = form.find('input', {'name':'account'})['value']
    post_data['passwd'] = form.find('input', {'name':'passwd'})['value']
    post_data['id'] = form.find('input', {'name':'id'})['value']
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request(YKT_RECHARGE_URL2, post_data)
    html = opener.open(req).read().decode('gbk')
    if '成功' in html:
        return True
    else:
        return False

def get_password_image(cookie):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    opener.open(YKT_TRY_URL)
    return opener.open(YKT_PASSWORD_PHOTO_URL).read()

def modify_password(cookie, old_password, new_password):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    opener.open(YKT_TRY_URL)
    soup = Soup(opener.open(YKT_MODIFY_PASSWORD_URL), from_encoding=CHARSET)
    account = soup.find('select').option['value']
    post_data = {'account':account, 'passwd':old_password, 'newpasswd':new_password, 'newpasswd2':new_password}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request(YKT_MODIFY_PASSWORD_URL2, post_data)
    html = opener.open(req).read().decode('gbk')
    if '成功' in html:
        return True
    else:
        return False

def report_loss(cookie, password):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    opener.open(YKT_TRY_URL)
    soup = Soup(opener.open(YKT_REPORT_LOSS_URL), from_encoding=CHARSET)
    account = soup.find('select').option['value']
    post_data = {'account':account, 'passwd':password}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request(YKT_REPORT_LOSS_URL2, post_data)
    html = opener.open(req).read().decode('gbk')
    if '成功' in html:
        return True
    else:
        return False
    
if __name__ == '__main__':
    from crawler import COOKIE
    from util import cookie_from_str
    cookie = cookie_from_str(COOKIE)
    print(crawl_ykt_information(cookie))
