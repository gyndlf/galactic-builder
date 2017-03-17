#This code will add a new varible(s) to all of the users in the data file.
#This is done according to database.py

import pickle
import os, sys

#Work out file paths
MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

#Work out file names
USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)
DATABASE = 'database.p'
DATABASEPATH = os.path.join(PICKLE_DIR, DATABASE)

#Load all the users currently made
with open(USERSPATH, 'rb') as f:
    users = pickle.load(f)

#Load database.p
with open(DATABASEPATH, 'rb') as f:
    data = pickle.load(f)

#For person in users change their varible(s)
for file in users:
    fname = os.path.join(PICKLE_DIR, file)
    print('')
    print("Opening " + str(fname))
    with open(fname, 'rb') as f:
        person = pickle.load(f)
    print(vars(person))

#Save the new database.py to the database.p file