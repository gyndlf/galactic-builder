# Creates a new user with no money, jobs or anything according to the database.py file

import pickle
import os, sys

import database

name = input("User name? ")
user = input("User id? ")

created = database.person

created.name = name
created.id = user

MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

filename = str(created.name) + ".p"

fname = os.path.join(PICKLE_DIR, filename)
print("Creating " + str(fname))
with open(fname, 'wb') as f:
    pickle.dump(created, f)
print("Created")


