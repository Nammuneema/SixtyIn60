from urllib import request
from urllib.request import urlopen, Request
from urllib.parse import urlsplit
from bs4 import BeautifulSoup

import html
import hashlib
import selector
import dbHelper as db
import os

req = urlopen('https://sports.ndtv.com/indian-premier-league-2017/ipl-2017-gautam-gambhir-says-kolkata-knight-riders-confident-of-chasing-any-target-1686529')
the_page = req.read().decode('utf-8')

selector = '[itemprop="articleBody"] p'
text = ""

soup = BeautifulSoup(the_page,"html.parser")
items = soup.select(selector)

for item in items:
    text = text + " ".join(item.text.split())

print(os.path.dirname(__file__))

