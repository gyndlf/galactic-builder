#This is the main python file.
#Please do not touch unless your are ABSOLUTELY SURE ABOUT WHAT YOU ARE DOING
#Thanks :)

#export FLASK_APP=mainpythonfile.py
#python -m flask run

import pickle
import os, sys

from flask import *
app = Flask(__name__)

networth = 300
money = 53

# Load all users according to "users.p" and display their stats

MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)

users = []

with open(USERSPATH, 'rb') as f:
    usersArray = pickle.load(f)

for file in usersArray:
    fname = os.path.join(PICKLE_DIR, file)
    print("Opening " + str(fname))
    with open(fname, 'rb') as f:
        peps = pickle.load(f)
        users.append(peps)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login/<string:user>')
def show_post(user):
    # show the post with the given id, the id is a string
    return "User = " + str(user)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):

    for person in users:
        if name == person.name:
            return render_template('finances.html', money=person.money, netIncome=person.netIncome, income=person.income, expenses=person.expenses, netWorth=person.netWorth)
    return "Invaild username"

if __name__ == "__main__":
    app.run()