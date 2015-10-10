'''
Created on 2015年9月1日

@author: wan
'''
from bs4 import BeautifulSoup as Soup
from spyne.model.complex import ComplexModel
from urllib.request import urlopen
from spyne import Unicode
from crawler import CHARSET


WEATHER_URL = 'http://www.weather.com.cn/weather/101280102.shtml'

class Weather(ComplexModel):
    week = Unicode
    date = Unicode
    weather = Unicode
    highest_temperature = Unicode
    lowest_temperature = Unicode
    wind = Unicode
    def __init__(self, week, date, weather, highest_temperature, lowest_temperature, wind):
        self.week, self.date, self.weather, self.highest_temperature, self.lowest_temperature, self.wind =\
         week, date, weather, highest_temperature, lowest_temperature, wind
         
def crawl():
    soup = Soup(urlopen(WEATHER_URL), from_encoding=CHARSET)
    div = soup.find('div', id='7d')
    weather_list = []
    for li in div.find_all('li'):
        week = li.find('h1').text
        date = li.find('h2').text
        weather = li.find('p', class_='wea').text
        highest_temperature = li.find('p', class_='tem tem1').text.strip()
        lowest_temperature = li.find('p', class_='tem tem2').text.strip()
        wind = li.find('p',class_='win').text.strip()
        weather_list.append(Weather(week, date, weather, highest_temperature, lowest_temperature, wind))
    return weather_list

if __name__ == '__main__':
    for item in crawl():
        print(item)