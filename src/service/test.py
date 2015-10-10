from suds.client import Client

from crawler import COOKIE


c = Client('http://192.168.202.225:8000/?wsdl')

print(c)
'''
with open('temp.png', 'wb') as file:
    file.write(bs)
'''
