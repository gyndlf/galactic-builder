# Removes a user from 'users.p' so you can delete their file

import pickle
import os, sys

import database

choice = False
name = str(input("User name? "))
if input('These changes are irreversible! Are you sure? (y/n)') == 'y' or input('These changes are irreversible! Are you sure? (y/n)') == 'Y':
    choice = True

if choice == False:
    quit()

users = []
MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')
USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)

filename = name + ".p"

with open(USERSPATH, 'rb') as f:
    users = pickle.load(f)

print("Removing " + name + " from " + USERS)
users.remove(filename)

print("Current users " + str(users))

with open(USERSPATH, 'wb') as f:
    pickle.dump(users, f)

print("Done")
print("You may now delete " + filename + ' safely.')


