import dbHelper as db
data = db.getLast(60)
for d in data:
	print(d['date'])
