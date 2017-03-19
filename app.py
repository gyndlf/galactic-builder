#This is the main python file.
#Please do not touch unless your are ABSOLUTELY SURE ABOUT WHAT YOU ARE DOING
#Thanks :)

#export FLASK_APP=mainpythonfile.py
#python -m flask run

import pickle
import os, sys
from flask import *
from functions import *

app = Flask(__name__)

message = ""
number = 0

# Load all users according to "users.p" and display their stats

MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)

users = []

#Load users from their .p files
with open(USERSPATH, 'rb') as f:
    usersArray = pickle.load(f)

for file in usersArray:
    fname = os.path.join(PICKLE_DIR, file)
    print("Opening " + str(fname))
    with open(fname, 'rb') as f:
        peps = pickle.load(f)
        users.append(peps)


#All app.route functions --------------#
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loginuser', methods=['POST'])
def calcmessage():
    username = request.form['username']
    print("Logging in to " + str(username))
    return redirect(url_for('user', name=username))

@app.route('/user/')
@app.route('/user/<name>')
def user(name=None):
    for person in users:
        if name == person.name:
            return render_template('finances.html',name=person.name, money=person.money, netIncome=person.netIncome, expenses=person.expenses)
    return "Invaild username"

@app.route('/user/<name>/button', methods=['POST'])
def userButton(name=None):
    global users
    for person in users:
        if name == person.name:
            print("Signed in as " + str(person.name))

            #Button detection below
            if True:
                #Finances.html -------------#
                #Farms ---------------------#
                if 'sellFarm' in request.form:
                    print("Detected 'sellFarm'")

                elif 'buyFarm' in request.form:
                    print("Detected 'buyFarm'")

                #Factories -----------------#
                elif 'sellCarFac' in request.form:
                    print("Detected 'sellCarFac'")

                elif 'buyCarFac' in request.form:
                    print("Detected 'buyCarFac'")

                elif 'sellUPFac' in request.form:
                    print("Detected 'sellUPFac'")

                elif 'buyUPFac' in request.form:
                    print("Detected 'buyUPFac'")

                elif 'sellAWFac' in request.form:
                    print("Detected 'sellAWFac'")

                elif 'buyAWFac' in request.form:
                    print("Detected 'buyAWFac'")

                elif 'sellToiletFac' in request.form:
                    print("Detected 'sellToiletFac'")

                elif 'buyToiletFac' in request.form:
                    print("Detected 'buyToiletFac'")

                elif 'sellPFFac' in request.form:
                    print("Detected 'sellPFFac'")

                elif 'buyPFFac' in request.form:
                    print("Detected 'buyPFFac'")

                #Mines --------------------#
                elif 'sellSteelMin' in request.form:
                    print("Detected 'sellSteelMin'")

                elif 'buySteelMin' in request.form:
                    print("Detected 'buySteelMin'")

                elif 'sellHydroMin' in request.form:
                    print("Detected 'sellHydroMin'")

                elif 'buyHydroMin' in request.form:
                    print("Detected 'buyHydroMin'")

                elif 'sellYECMin' in request.form:
                    print("Detected 'sellYECMin'")

                elif 'buyYECMin' in request.form:
                    print("Detected 'buyYECMin'")

                elif 'sellTitMin' in request.form:
                    print("Detected 'sellTitMin'")

                elif 'buyTitMin' in request.form:
                    print("Detected 'buyTitMin'")

                elif 'sellSiliconMin' in request.form:
                    print("Detected 'sellSiliconMin'")

                elif 'buySiliconMin' in request.form:
                    print("Detected 'buySiliconMin'")

                elif 'sellCopMin' in request.form:
                    print("Detected 'sellCopMin'")

                elif 'buyCopMin' in request.form:
                    print("Detected 'buyCopMin'")

                elif 'sellNoobMin' in request.form:
                    print("Detected 'sellNoobMin'")

                elif 'buyNoobMin' in request.form:
                    print("Detected 'buyNoobMin'")

                elif 'sellDiaMin' in request.form:
                    print("Detected 'sellDiaMin'")

                elif 'buyDiaMin' in request.form:
                    print("Detected 'buyDiaMin'")

                elif 'sellHeMin' in request.form:
                    print("Detected 'sellHeMin'")

                elif 'buyHeMin' in request.form:
                    print("Detected 'buyHeMin'")

                elif 'sellWHCMin' in request.form:
                    print("Detected 'sellWHCMin'")

                elif 'buyWHCMin' in request.form:
                    print("Detected 'buyWHCMin'")

                #Research ---------------------#
                elif 'buyLCR' in request.form:
                    print("Detected 'buyLCR'")

                elif 'buyBFR' in request.form:
                    print("Detected 'buyBFR'")

                elif 'buyNKR' in request.form:
                    print("Detected 'buyNKR'")

                elif 'buyRWR' in request.form:
                    print("Detected 'buyRWR'")

                else:
                    print('Unknown value')

    print("Redirect")
    return redirect(url_for('user', name=name))

if __name__ == "__main__":
    app.run()