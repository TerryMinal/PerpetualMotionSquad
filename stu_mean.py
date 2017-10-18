'''
Perpetual Motion Squad - Terry Guan and Charles Weng
SoftDev1 pd 7
HW09 -- No Treble
2017-10-16

Be sure to run makeDB.py before this for the database
'''
import sqlite3

try:
    import makeDB
except:
    print "DB already created... moving on\n"

# initialize database
db = sqlite3.connect("data.db")
c = db.cursor()

# helpers for neatly printing out the given dictionary of lists or regular dictionary respectively
def print_listdic(dic):
    # loop through each key and print it out
    for student in dic:
        # construct printing string
        x = student + ": ["
        for value in dic[student]:
            x += " " + str(value)
        print x + " ]"

def print_dic(dic):
    # loop through each key and print it out
    for student in dic:
        x = student + ": " + str(dic[student])
        print x

#return a dictionary in the format {name: id}
def get_id():
    f = 'SELECT name, id FROM peeps'
    x = c.execute(f)
    ret_dict = {}
    for line in x:
        ret_dict[line[0]] = line[1]
    return ret_dict

# helper function that returns a dictionary int the format {<name>: [grade1, grade2 ...]}
def get_grades():
    # get the raw data from the sqlite3
    foo = 'SELECT name, grade FROM peeps, courses WHERE peeps.id = courses.id'
    x = c.execute(foo)
    # process the data into a dictionary of lists
    grades = {}
    for line in x:
        # check if there is a list in grades for the student
        if line[0] not in grades:
            grades[line[0]] = []
        # add in the grade to the list for the student
        grades[line[0]].append(line[1])
    return grades

# print "Grades:"
# print_listdic(get_grades())

# helper that returns the average value of a list of ints
def average(x):
    sum = 0
    for value in x:
        sum += value
    return sum / len(x)

# process each student's grades into a dict of averages. {name: avg}
def get_averages():
    grades = get_grades()
    averages = {}
    for student in grades:
        averages[student] = average(grades[student])
    return averages

# print "\nAverages:"
# print_dic(get_averages())

def display():
    avg = get_averages()
    ID = get_id()
    for name in ID.keys():
        print name + ", " + str(ID[name]) + ", " + str(avg[name])
    return
#display()

def initialize_table_avg():
    avg = get_averages()
    ID = get_id()
    for name in ID.keys():
        x = "INSERT INTO peeps_avg VALUES(" + str(ID[name]) +"," + str(avg[name]) + ")"
        c.execute(x)
    db.commit()
    print "db peeps_avg intialized..."
    return

initialize_table_avg()

def update_table_avg():
    avg = get_averages()
    ID = get_id()
    for name in ID.keys():
        x = "UPDATE peeps_avg SET average = " + str(avg[name]) + " WHERE id = " + str(ID[name])
        c.execute(x)
    db.commit()
    print "peeps_avg updated..."
    return

# update_table_avg()

def add_row(course, avg, ID):
    x = "INSERT INTO courses VALUES(" + "'" + course + "'" + "," + str(avg) + "," + str(ID) + ")"
    print x
    c.execute(x)
    db.commit()
    update_table_avg()
    return

add_row("softdev", 20, 1)
