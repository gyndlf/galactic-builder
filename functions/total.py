#Total Varibles recipie book

#These are things like total food sent, total net worth

import pickle
import os, sys

MY_DIR  = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)

with open(USERSPATH, 'rb') as f:
    users = pickle.load(f)

print('Current users ' + str(users))

for file in users:
    fname = os.path.join(PICKLE_DIR, file)
    #print('')
    print("Opening " + str(fname))
    with open(fname, 'rb') as f:
        person = pickle.load(f)
    #print(vars(person))


class farm ():
    def __init__(self):
        print('Calculating total dynamic varibles')

        #Farms
        #self.totalFoodSent
