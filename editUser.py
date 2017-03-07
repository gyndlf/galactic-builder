# Load the specified user
import pickle
import os, sys

#Create file path
MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

#Create file name
name = str(input("Username? "))
filename = name + ".p"

#Finish making file path
fname = os.path.join(PICKLE_DIR, filename)
print("Opening " + str(fname))

#Open and save the varible from the file
with open(fname, 'rb') as f:
    person = pickle.load(f)

print("Loaded user " + person.name)

edit = str(input("Varible to edit? "))
value = person.edit
print("Current value is " + value)
