# Load all users according to "users.p" and display their stats
import pickle
import os, sys

MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)

with open(USERSPATH, 'rb') as f:
    users = pickle.load(f)

print('Current users ' + str(users))

for file in users:
    fname = os.path.join(PICKLE_DIR, file)
    print('')
    print("Opening " + str(fname))
    with open(fname, 'rb') as f:
        person = pickle.load(f)
    print(vars(person))