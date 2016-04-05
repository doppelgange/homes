#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="homes")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("INSERT INTO `test` (`uuid`, `full_address`, `google_street_view_url`) VALUES ( 'B', 'B', 'B');")
db.commit()

cur.execute("SELECT * FROM test")

# print all the first cell of all the rows
for row in cur.fetchall():
    print row[1]

db.close()
