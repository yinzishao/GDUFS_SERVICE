from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, Byte, Boolean
from spyne.model.complex import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from crawler import CET_score_crawler, course_crawler, score_crawler, news_crawler, weather_crawler,\
    information_crawler, ykt_crawler
import crawler
from util import cookie_from_str


class GDUFSService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def login(self, username, password):
        cookie = crawler.login(username, password)
        if cookie:
            return cookie.as_lwp_str()
        else:
            return ''
    @rpc(Unicode, Unicode, _returns=Iterable(CET_score_crawler.CETScore))
    def crawl_CET_score(self, cookie, student_number):
        return CET_score_crawler.crawl(cookie_from_str(cookie), student_number)
    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Iterable(Iterable(course_crawler.Course)))
    def crawl_course(self, cookie, student_number, year, term):
        return course_crawler.crawl(cookie_from_str(cookie), student_number, year, term)
    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Iterable(score_crawler.Score))
    def crawl_score(self, cookie, student_number, year, term):
        return score_crawler.crawl(cookie_from_str(cookie), student_number, year, term)
    @rpc(Integer, _returns=Iterable(news_crawler.News))
    def crawl_news(self, page):
        return news_crawler.crawl(news_crawler.NEWS, page)
    @rpc(Integer, _returns=Iterable(news_crawler.News))
    def crawl_announcement(self, page):
        return news_crawler.crawl(news_crawler.ANNOUNCEMENT, page)
    @rpc(_returns=Iterable(weather_crawler.Weather))
    def crawl_weather(self):
        return weather_crawler.crawl()
    @rpc(Unicode, _returns=information_crawler.Information)
    def crawl_information(self, cookie):
        return information_crawler.crawl(cookie_from_str(cookie))
    @rpc(Unicode, _returns=ykt_crawler.YKTInformation)
    def crawl_ykt_information(self, cookie):
        return ykt_crawler.crawl_ykt_information(cookie_from_str(cookie))
    @rpc(Unicode, _returns=Iterable(ykt_crawler.Account))
    def crawl_today_account(self, cookie):
        return ykt_crawler.crawl_today_account(cookie_from_str(cookie))
    @rpc(Unicode, Unicode, Unicode, _returns=Iterable(ykt_crawler.Account))
    def crawl_history_account(self, cookie, start_day, end_day):
        return ykt_crawler.crawl_history_account(cookie_from_str(cookie), start_day, end_day)
    @rpc(Unicode, Integer, Unicode, _returns=Boolean)
    def recharge(self, cookie, money, password):
        return ykt_crawler.recharge(cookie_from_str(cookie), money, password)
    @rpc(Unicode, _returns=Iterable(Byte))
    def get_password_image(self, cookie):
        return ykt_crawler.get_password_image(cookie_from_str(cookie))
    @rpc(Unicode, Unicode, Unicode, _returns=Boolean)
    def modify_password(self, cookie, old_password, new_password):
        return ykt_crawler.modify_password(cookie_from_str(cookie), old_password, new_password)
    @rpc(Unicode, Unicode, _returns=Boolean)
    def report_loss(self, cookie, password):
        return ykt_crawler.report_loss(cookie_from_str(cookie), password)
if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    application = Application([GDUFSService], 'gdufs.service',
                              in_protocol=Soap11(),
                              out_protocol=Soap11())
    # server = make_server('192.168.202.225', 8000, WsgiApplication(application))
    server = make_server('192.168.1.85', 8000, WsgiApplication(application))
    server.serve_forever()