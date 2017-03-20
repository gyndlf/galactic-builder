#This code will add a new varible(s) to all of the users in the data file.
#This is done according to database.py

import pickle
import os, sys
import database
import baseValues


confirm = False
print('You are about to update the entire database. If this goes wrong EVERYTHING WILL BE LOST. Triple check before contuning')
print('You cannot remove varibles (yet) only add so everything is PERMENENT!')
print('Edit "database.py" to update the varibles. Be CAREFUL!')
if str(input('Are you sure you want to continue? ')) == 'y':
    confirm = True
if confirm == False:
    quit()

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
    oldData = pickle.load(f)
oldVars = vars(oldData)

#Load new database
newData = database.person()
newVars = vars(newData)

#Find the changes
change = []
for varible in newVars:
    try:
        oldVars[varible]
    except:
        change.append(varible)

print('Differences in databases ' + str(change))

#For person in users change their varible(s)
for file in users:
    fname = os.path.join(PICKLE_DIR, file)
    print('')
    print("Opening " + str(fname))

    #Open the file
    with open(fname, 'rb') as f:
        person = pickle.load(f)

    #Find person current varibles
    current = vars(person)
    print("Old : " + str(current))

    #Add changes
    for diff in change:
        print("Need to add " + diff)
        current[diff] = 0

    print("New : " + str(current))

    with open(fname, 'wb') as f:
        pickle.dump(person, f)


#Save the new database.py to the database.p file
print('')
print('Saving new database...')
with open(DATABASEPATH, 'wb') as f:
    pickle.dump(newData, f)


#Do the same with the values:
print('')
print("Moving on to values.p")

#Work out names
VALUES = 'values.p'
VALUESPATH = os.path.join(PICKLE_DIR, VALUES)

#Load values.p
with open(VALUESPATH, 'rb') as f:
    oldValues = pickle.load(f)
oldVarsv = vars(oldValues)

#Load new values
newValues = baseValues.basic()
newVarsv = vars(newValues)

#Find the changes
changes = []
for varible in newVarsv:
    try:
        oldVarsv[varible]
    except:
        changes.append(varible)

print("Found " + str(changes) + ' changes.')
print('Old : ' + str(oldVarsv))

#Add changes
for diff in changes:
    print("Need to add " + diff)
    oldVarsv[diff] = 0

print("New : " + str(oldVarsv))

with open(VALUESPATH, 'wb') as f:
    pickle.dump(newValues, f)

print('Done.')