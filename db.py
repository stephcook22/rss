import MySQLdb
from datetime import datetime
import calendar


def getConnection():
    return MySQLdb.connect(host="example.com",  # your host, usually localhost
                     user="user",  # your username
                      passwd="password",  # your password
                      db="database")  # name of the data base

# you must create a Cursor object. It will let
#  you execute all the query you need

def cleardb(db):
    db.ping(True)
    cur=db.cursor()
    cur.execute("""TRUNCATE TABLE stories""")
    cur.execute("""TRUNCATE TABLE additions""")
    db.commit()


def addStory(title, text, desc, db):
    db.ping(True)
    cur=db.cursor()
    now = datetime.utcnow()
    now = calendar.timegm(now.utctimetuple())
    data = {
    'title': unicode(title).encode('utf-8'),
    'text': unicode(text).encode('utf-8'),
    'now': now,
    'desc': unicode(text).encode('utf-8')
}

    cur.execute("""INSERT INTO stories (Title, Text, Description, LastUpdated) VALUES(%(title)s, %(text)s, %(desc)s, %(now)s)""", data)
    db.commit()
    return cur.lastrowid


def appendStory(storyid, text, db):
    db.ping(True)
    cur=db.cursor()
    data = {
    'id': storyid,
    'text': str(text).encode('utf-8'),
    'algorithm': 1
}
    now = datetime.utcnow()
    now = calendar.timegm(now.utctimetuple())
    data2 = {'id': storyid, 'now': now}

    cur.execute("""INSERT INTO additions (StoryID, Text, algorithm) Values (%(id)s, %(text)s, %(algorithm)s)""", data)
    cur.execute("""UPDATE stories SET LastUpdated=%(now)s where id=%(id)s""", data2)
    db.commit()


