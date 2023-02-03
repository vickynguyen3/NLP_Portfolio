# Vicky Nguyen, vtn180004
# CS 4395.001
# Homework 1 Portfolio Assignment 1: Text Processing

import sys
import pathlib
import re
import pickle


# define person class w/ fields: last, first, mi, id, and phone 
# in addition to init method, create a display() method to output fields
class Person:

    # init method
    def __init__(self, firstName, lastName, mi, id, phoneNum):
        self.firstName = firstName
        self.lastName = lastName
        self.mi = mi
        self.id = id
        self.phoneNum = phoneNum
    
    # display method
    def display(self):
        print('Employee id:' + id)

# modify last name and first name to be in Capital Case, if necessary
def modName(name):
    return name.capitalize()

# modify middle initial to be a single upper case letter, if necessary
# use 'X' as a middle initial if one is missing
def modMi(mi):
    if not mi:
        return 'X'
    else:
        return mi.capitalize()

# modify id if necessary, using regex. Id should be 2 letters
    # followed by 4 digits. if an id is not in the correct format, output an error
    # msg, and allow user to re-enter a valid ID
def modId(id):
    return id

# modify phone number, if necessary, to be in form 999-999-9999. use regex
def modPhoneNum(phoneNum):
    return phoneNum

# create function to process input file, get rid of the first line which is the heading line
def processFile(txt_in):

    # split on comma to get fields
    for line in txt_in:
        fields = line.split(',')

    # modify first, last, mi, id, phone number if necessary
    firstName = modName(fields[1])
    lastName = modName(fields[0])
    mi = modMi(fields[2])
    id = modId(fields[3])
    phoneNum = modPhoneNum(fields[4])
    

    # once data for a person is correct, create a Person object and save the object to a dict of persons
    # where id is the key. check for duplicate id and print and error msg if an id is repeated in the file

    # return the dict of persons to the main function
    return



# ----------- main -----------
if __name__ == '__main__':
    
    # check if there's a sysarg
    if len(sys.argv) < 2:
        # print error msg and quit program
        print('Please enter a file name as a system arg')
        quit()

    # user specifies relative path in a sysarg
    rel_path = sys.argv[1]

    # read in data and close file
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as file:
        txt_in = file.read().splitlines()

    # call process function and ignore the header line
    # place all people from data input into 'employees' dict 
    employees = processFile(txt_in[1:])

    # pickle file, write back
    pickle.dump(employees, open('employees.pickle', 'wb'))

    # unpickle file, read back
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    # print employee list to check if successful unpickle
    print('\n\nEmployee list:')

    for id in employees_in:
        employees_in[id].display()