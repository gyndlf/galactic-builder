# This code will initilise the database You probably will run it when you start from scratch

import pickle
import os, sys
import database

confirm = False
print('This script will create "database.p" and "users.p".')
print('If you have edited "database.py" and not run "updateVaribles.py" all your changes will be lost and you will have to wipe the database.')
if str(input('Are you sure you want to continue? ')) == 'y':
    confirm = True
if confirm == False:
    quit()

# Work out file paths
MY_DIR = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

DATABASE = 'database.p'
DATABASEPATH = os.path.join(PICKLE_DIR, DATABASE)

USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)

users = []
with open(USERSPATH, 'wb') as f:
    pickle.dump(users, f)

# Load database.p
data = database.person()

with open(DATABASEPATH, 'wb') as f:
    pickle.dump(data, f)

print("Done.")