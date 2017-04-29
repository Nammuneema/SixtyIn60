from urllib import request
from urllib.request import urlopen, Request
from urllib.parse import urlsplit
from bs4 import BeautifulSoup as bs
import hashlib
import re

def hashId(string):
    md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
    return md5

def getDomain(url):
    base_url = "{0.netloc}".format(urlsplit(url))
    return base_url

def cleanText(data):
    text = " ".join(data.split())
    text = text.replace('. ', '.')
    # this add space after fullstop in paragraph
    text = ". ".join(text.split('.'))
    # change line ending with . " => ."
    text = text.replace('. "', '." ')
    text = text.replace(". '", ".' ")

    return text

def getHTML(url):
    # Required to spoof some of the sites which otherwise don't return data
    userAgent = "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"
    req = Request(url, headers={'User-Agent': userAgent})
    res = urlopen(req)
    the_page = res.read().decode('utf-8')
    return the_page

def filterUnwantedTag(unFiltered):
    regex = re.compile(r'<(script|blackquote).*?</\1>(?s)') #'<(script|blackquote|xyz).*?</\1>(?s)'
    filtered = re.sub(regex, "", unFiltered)

    return filtered
