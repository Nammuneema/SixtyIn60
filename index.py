from urllib import request
from urllib.request import urlopen, Request
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

import html.parser
import hashlib
import selector
import dbHelper as db

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

        # extract title and image from meta
        #article['title'] = soup.find("meta", property="og:title")['content']
        article['image'] = soup.find("meta", property="og:image")['content']

        for item in items:
            text = text + " ".join(item.text.split())

        text = text.replace('. ', '.')
        # this add space after fullstop in paragraph
        article['body'] = ". ".join(text.split('.'))
        # change line ending with . " => ."
        text = text.replace('. "', '."')
        text = text.replace(". '", '.')
    else:
        print('no selector for this site: '+url)

    return article

def getNews():

    req = urlopen('https://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&output=rss')
    the_page = req.read().decode('utf-8')

    soup = BeautifulSoup(the_page,"html.parser")
    items = soup.find_all('item')

    for item in items:

        # unescape html entitiles
        htmlParser = html.parser.HTMLParser()
        title = htmlParser.unescape(item.find('title').text)
        # remove website name from title
        parts = title.split(' - ')
        parts = parts[:-1]
        title = "-".join(parts)
        source = parts[len(parts)-1]

        url = item.find('link').text
        link = url.split('url=')[1]

        date = item.find('pubdate').text
        category = item.find('category').text

        try:
            article = getArticle(link)
            article['title'] = title
            article['date'] = date
            article['category'] = category
            article['source'] = source

            if article['body'] != "":
                db.insert(article)

            print(article['title'])
            print(article['date'])
            print(article['link'])

        except:
            print('error while fetching: '+link+'\n')

if __name__ == '__main__':
    getNews()