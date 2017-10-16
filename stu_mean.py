'''
Perpetual Motion Squad - Terry Guan and Charles Weng
SoftDev1 pd 7
HW09 -- No Treble
2017-10-16
'''
import sqlite3

# initialize database
db = sqlite3.connect("data.db")
c = db.cursor()

# helpers for neatly printing out the given dictionary of lists or regular dictionary respectively
def print_listdic(dic):
    # loop through each key and print it out
    for student in dic:
        x = student + ": ["
        for value in dic[student]:
            x += " " + str(value)
        print x + " ]"
def print_dic(dic):
    # loop through each key and print it out
    for student in dic:
        x = student + ": " + str(dic[student])
        print x


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

print "Grades:"
print_listdic(get_grades())

# helper that returns the average value of a list of ints
def average(x):
    sum = 0
    for value in x:
        sum += value
    return sum / len(x)

# process each student's grades into a dict of averages
def get_averages():
    grades = get_grades()
    averages = {}
    for student in grades:
        averages[student] = average(grades[student])
    return averages

print "\nAverages:"
print_dic(get_averages())

def display():
    pass
