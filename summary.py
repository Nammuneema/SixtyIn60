from urllib.request import urlopen, Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup

url = 'http://66.246.138.35/bin/sumplify'

def summerise(article, sentense):
    values = {'texto' : article, 'frases'  : sentense, 'email':'gh@we.cyk'}
    data = urlencode(values)
    data = data.encode('utf-8') # data should be bytes
    req = Request(url, data)
    response = urlopen(req)
    the_page = response.read().decode('utf-8')
    soup = BeautifulSoup(the_page, "html.parser")
    items = soup.select('p')[3]
    return items.text

def getSummary(article):
    text = ""
    sentense = 5
    count = 70

    if len(article) == 0:
        print(">> Summary : Article length is 0")
        raise Exception()

    while count > 50 and sentense > 0:
        text = summerise(article,sentense)
        count = len(text.split(' '))
        sentense = sentense - 1
        # print("itr:"+str(sentense))

    return text
