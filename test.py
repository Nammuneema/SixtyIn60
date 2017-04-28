from urllib import request
from urllib.request import urlopen, Request
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

import html.parser
import hashlib
import selector
import dbHelper as db
import summary

selectors = selector.getSelectors()

# Required to spoof some of the sites which otherwise don't return data
userAgent = "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"

def hashId(string):
    md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
    return md5

def getDomain(url):
    base_url = "{0.netloc}".format(urlsplit(url))
    return base_url

def getArticle(url):
    domain = getDomain(url)
    text = ""

    article = {
        'id':hashId(url),
        'title':'',
        'body':'',
        'image':'',
        'source':'',
        'link':url,
        'date':'',
        'category':''
    }

    if domain in selectors.keys():
        req = Request(url, headers={'User-Agent': userAgent})
        res = urlopen(req)
        the_page = res.read().decode('utf-8')
        soup = BeautifulSoup(the_page, "html.parser")

        # get the selector for this perticular site.
        selector = selectors[domain]
        items = soup.select(selector)
        
        print(selector)
        print(soup.prettify())
        print(items)

        # extract title and image from meta
        #article['title'] = soup.find("meta", property="og:title")['content']
        article['image'] = soup.find("meta", property="og:image")['content']

        for item in items:
            text = text + " ".join(item.text.split())
        
        print("\n"+text+"\n")

        text = text.replace('. ', '.')
        # this add space after fullstop in paragraph
        text = ". ".join(text.split('.'))
        # change line ending with . " => ."
        text = text.replace('. "', '." ')
        text = text.replace(". '", ".' ")
        #try:
        article['body'] = summary.getSummary(text)
        print(article['body'])
        #except:
            #print('>> Error while generating summary')
    else:
        print('no selector for this site: '+url)

    return article

getArticle('http://www.indiatvnews.com/news/india-sukma-attack-retaliation-for-2016-encounters-say-maoists-379192')

    