'''
Charles Weng
SoftDev1 pd 7
HW09 -- No Treble
2017-10-16

My hw was the simpler of the two and thus we used it to help keep clear what this script does
'''
import csv, sqlite3

# initialize database
db = sqlite3.connect("data.db")
c = db.cursor()

# add in the two tables
c.execute("CREATE TABLE peeps (name TEXT, age INTEGER, id INTEGER PRIMARY KEY)")
c.execute("CREATE TABLE courses (course TEXT, grade INTEGER, id INTEGER)")
c.execute("CREATE TABLE peeps_avg (id INTEGER, average INTEGER)")

# open the two files
csv1  = csv.DictReader(open("peeps.csv"))
csv2 = csv.DictReader(open("courses.csv"))

# enter in the csv values
for row in csv1:
    # print row
    c.execute("INSERT INTO peeps VALUES ('" + row['name'] + "', " + row['age'] + ", " + row['id'] + ")")
# print "completed adding peeps.csv"
for row in csv2:
    # print row
    c.execute("INSERT INTO courses VALUES ('" + row['code'] + "', " + row['mark'] + ", " + row['id'] + ")")
# print "completed adding courses.csv"

# save and close database
db.commit()
db.close()
