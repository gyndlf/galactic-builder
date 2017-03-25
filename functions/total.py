#Total Varibles recipie book

#These are things like total food sent, total net worth
print('total.py')
import pickle
import os, sys

MY_DIR  = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)

with open(USERSPATH, 'rb') as f:
    users = pickle.load(f)

print('Current users ' + str(users))

people = []

for file in users:
    #Find file name
    fname = os.path.join(PICKLE_DIR, file)
    #Open the file and save
    print("Opening " + str(fname))
    with open(fname, 'rb') as f:
        person = pickle.load(f)

    #Save person
    people.append(person)
    #print(vars(person))


class total ():
    def __init__(self):
        print('Calculating total dynamic varibles')

        #Farms
        self.foodSent = 0
        for person in people:
            self.foodSent += person.foodProduced

        #Money
        self.totalMoney = 0
        for person in people:
            self.totalMoney += person.money

        print(self.foodSent, self.totalMoney)
