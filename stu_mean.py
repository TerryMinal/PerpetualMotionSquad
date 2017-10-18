'''
Perpetual Motion Squad - Terry Guan and Charles Weng
SoftDev1 pd 7
HW09 -- No Treble
2017-10-17
'''
import sqlite3, csv


try:
    import makeDB
    print "DB created...\n"
except:
    print "DB already created... \n"


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

# states if repective database table needs updated
# initialized as false to force an update at run
# set this to True again whenever the csv files are changed by this script (we don't)
# peeps shouldn't change so it doesn't need one
course_update = True

# helper function that returns a dictionary int the format {<name>: [grade1, grade2 ...]}
def get_grades():
    # if you need an update then update
    if course_update:
        update_table_courses()

    # get the table from the database
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

# tries to reinsert all the values from courses.csv
def update_table_courses():
    courses = csv.DictReader(open("courses.csv"))
    for row in courses:
        # PRIMARY KEY is the pair (id, courses) so if they're not unique it returns an error for unique constraint
        try:
            c.execute("INSERT INTO courses VALUES ('" + row['code'] + "', " + row['mark'] + ", " + row['id'] + ")")
        except:
            c.execute("UPDATE courses SET grade = "  + row['mark'] + " WHERE course = '" + row['code'] + "' and id = " + row['id'])
    db.commit()
    global course_update
    course_update = False
    print "courses updated..."
    # average relies on the course grades so if they change then natually average changes
    update_table_average()

# updates the table <id, average>
def update_table_average():
    ID = get_id()
    avg = get_averages()
    for name in ID.keys():
        # try to insert the student's value except when insert isn't unique
        try:
            x = "INSERT INTO peeps_avg  VALUES(id = " + str(ID[name]) + "average = " + str(avg[name]) + ")"
            c.execute(x)
        except:
            x = "UPDATE peeps_avg SET average = " + str(avg[name]) + " WHERE id = " + str(ID[name])
            c.execute(x)
    db.commit()

# process each student's grades into a dict of averages. {name: avg}
def get_averages():
    grades = get_grades()
    averages = {}
    for student in grades:
        averages[student] = average(grades[student])
    return averages

# helper that returns the average value of a list of ints
def average(x):
    sum = 0
    for value in x:
        sum += value
    return sum / len(x)



def display():
    avg = get_averages()
    ID = get_id()
    for name in ID.keys():
        print name + ", " + str(ID[name]) + ", " + str(avg[name])
    return
    #display()

# print "id:"
# print_dic(get_id())
# print "\nGrades:"
# print_listdic(get_grades())
# print "\nAverages:"
# print_dic(get_averages())
# print "\n"
display()

# testing for primary key insertion
def add_row(course, avg, ID):
    x = "INSERT INTO courses VALUES(" + "'" + course + "'" + "," + str(avg) + "," + str(ID) + ")"
    print x
    c.execute(x)
    update_table_average()
    return

# add_row("softdev", 20, 1)
db.close()
