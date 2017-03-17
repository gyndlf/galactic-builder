# This code will add a new varible(s) to all of the users in the data file.
# This is done according to database.py

import pickle
import os, sys
import database


# Work out file paths
MY_DIR = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

# Work out file names
DATABASE = 'database.p'
DATABASEPATH = os.path.join(PICKLE_DIR, DATABASE)

# Load database.p
data = database.person()

with open(DATABASEPATH, 'wb') as f:
    pickle.dump(data, f)

print("Done.")