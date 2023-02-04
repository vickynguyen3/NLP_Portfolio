# Vicky Nguyen, vtn180004
# CS 4395.001
# Homework 1: Text Processing

import sys
import pathlib
import re
import pickle


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

# modify last name and first name to be capitalized
def modName(name):
    return name.capitalize()

# modify middle name
def modMi(mi):
    # if mi is missing, input 'X' otherwise capitalize
    if not mi:
        return 'X'
    else:
        return mi.capitalize()

# modify ID 
def modId(id):

    # regex, ID correct format: 2 letters followed by 4 digits
    if re.search('[a-zA-Z][a-zA-Z]\d\d\d\d', id) and len(id) == 6:
        return id
    else:
        # ID not in correct format, output an error msg
        # allow user to input a valid ID
        id = input('ID invalid: ' + id 
        + '\nID is two letters followed by 4 digits'
        + '\nPlease enter a valid id: ')
    return modId(id)

# modify phone number, if necessary
def modPhoneNum(phoneNum):

    # regex, phone number correct format: 999-999-9999
    if re.search('\d\d\d-\d\d\d-\d\d\d\d', phoneNum) and len(phoneNum) == 12:
        return phoneNum
    else:
        # phone number not in correct format, output error msg
        # allow user to input a valid phone number
        id = input('Phone: ' + phoneNum + 'is invalid'
        + '\nEnter phone number in the form 123-456-7890'
        + '\nEnter phone number: ')
    return modPhoneNum(phoneNum)

# check for duplicate id and print and error msg if an id is repeated in the file
def checkDup(dict, key):
    if 
    return False

# create function to process input file, get rid of the first line which is the heading line
def processFile(txt_in):

    # split on comma to get fields
    for line in txt_in:
        fields = line.split(',')

    # modify first, last, mi, id, phone number if necessary
    firstName = modName(fields[1])
    mi = modMi(fields[2])
    lastName = modName(fields[0])
    id = modId(fields[3])
    #phoneNum = modPhoneNum(fields[4])
    

    # once data for a person is correct, create a Person object and save the object to a dict of persons
    # where id is the key. 

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

    # for id in employees_in:
    #    employees_in[id].display()