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

value = getattr(person,edit)
print("Current value is " + str(value))

kind = input("Is this new value a string or int (s or i)? ")

if kind == "s" or kind == "S":
    new = str(input("What should the new value be? "))
elif kind == "i" or kind == "I":
    new = int(input("What should the new value be? "))
else:
    print("Invaild option.")
    exit()

setattr(person,edit,new)

check = getattr(person,edit)
print("Updated the value to " + str(check))

with open(fname, 'wb') as f:
    pickle.dump(person, f)

print("Done.")