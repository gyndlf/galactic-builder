# Creates a new user with no money, jobs or anything according to the "database.py" file and add them into a list stored in "users.p"

import pickle
import os, sys

import database

name = input("User name? ")
user = input("User id? ")
users = []

created = database.person()

created.name = name
created.id = user

MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')
USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)

filename = str(created.name) + ".p"
fname = os.path.join(PICKLE_DIR, filename)
print("Creating " + str(fname))

with open(USERSPATH, 'rb') as f:
    users = pickle.load(f)
#users = []
print("Adding " + name + " to " + USERS)
users.append(filename)
print("Current users " + str(users))
with open(USERSPATH, 'wb') as f:
    pickle.dump(users, f)


with open(fname, 'wb') as f:
    pickle.dump(created, f)
print("Created")
print("Done")


