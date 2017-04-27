from tinydb import TinyDB, Query
import datetime
import os

path = os.path.dirname(__file__)+'/db.json'

def getAll():
    with TinyDB(path) as db:
        return db.all()

def getLast(num):
    data = []
    with TinyDB(path) as db:
        arr = sorted(db.all(), key=_sortByDate)
        if len(arr) > num:
            for i in range(num):
                data.append(arr[i])
            return data
        else:
            return arr

def _sortByDate(item):
    t1 = datetime.datetime.now()
    t2 = datetime.datetime.strptime(item['date'], "%a, %d %b %Y %X %Z")
    dt = t1-t2
    time = divmod(dt.days * 86400 + dt.seconds, 60)
    return time[0]


def insert(data):
    with TinyDB(path) as db:
        news = Query()
        if db.contains(news.id == data['id']) is False:
            db.insert(data)
        else:
            print('dbHelper : data already exist')


