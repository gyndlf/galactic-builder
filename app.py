#This is the main python file.
#Please do not touch unless your are ABSOLUTELY SURE ABOUT WHAT YOU ARE DOING
#Thanks :)

#export FLASK_APP=mainpythonfile.py
#python -m flask run

import pickle
import os, sys
from flask import *

app = Flask(__name__)

message = ""
number = 0

toBeSaved = {}

# Load all users according to "users.p" and display their stats

MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)

users = []

def printVars (object):
    print(str(object) + " vars: " + str(vars(object)))

def loadUsers ():
    # Load users from their .p files
    with open(USERSPATH, 'rb') as f:
        usersArray = pickle.load(f)

    for file in usersArray:
        fname = os.path.join(PICKLE_DIR, file)
        #print("Opening " + str(fname))
        with open(fname, 'rb') as f:
            peps = pickle.load(f)
            users.append(peps)
    return users

def saveUsers ():
    pass

def hasMoney (object, money):
    try:
        if object.money >= money:
            return True
        else:
            return False
    except:
        return False

def dynamicPersonalCalc (object):
    #Calculate personal dynamic varibles
    from functions import farms, factories, mines
    farmsClass = farms.farm()

    #Farms
    Fproduced = object.farmLevel * object.numberFarms
    Fincome = Fproduced * farmsClass.farmValue

    income = Fincome + 0 #Add factory income and mine income here
    expenses = int(income/5) #(Tax) Add all expenses here
    netIncome = income - expenses

    calculated = {
        'Fproduced' : Fproduced,
        'Fincome' : Fincome,
        'income' : income,
        'expenses' : expenses,
        'netIncome' : netIncome
    }

    #Save new varibles
    username = object.name + '.p'
    fname = os.path.join(PICKLE_DIR, username)
    with open(fname, 'wb') as f:
        pickle.dump(object, f)

    return calculated

def total ():
     # These are things like total food sent, total net worth
    users = loadUsers()

    foodSent = 0
    totalMoney = 0
    for person in users:
        foodSent += person.foodProduced
        totalMoney += person.money

    calculated = {
        'foodSent' : foodSent,
        'totalMoney' : totalMoney
    }
    return calculated

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
    from functions import farms, factories, mines

    #Calculate the recipies
    print('Calculating dynamic varibles...')
    farmsClass = farms.farm()
    totals = total()

    #Load all the users
    print('Loading all users...')
    users = loadUsers()

    #Identify the user
    for person in users:
        if name == person.name:
            #printVars(person)
            #printVars(farmsClass)

            #Calculate dynamic personal varibles
            print('Calculating dynamic personal varibles...')
            dynamicPersonal = dynamicPersonalCalc(person)

            #Test it
            print('Income $' + str( dynamicPersonal['income']))
            print('You are sending ' + str(totals['foodSent']) + ' bits of food.')

            #Return the html
            return render_template('basicFinances.html',name=person.name, money=person.money, netIncome=dynamicPersonal['netIncome'],
                                   farmIncome=dynamicPersonal['Fincome'], numOfFarms=person.numberFarms, amountProduced=dynamicPersonal['Fproduced'],
                                   farmCost=farmsClass.farmCost, farmLevel=person.farmLevel, farmLevelCost=farmsClass.levelCost, farmValue=farmsClass.farmValue)
    return "Invaild username"

@app.route('/user/<name>/button', methods=['POST'])
def userButton(name=None):
    from functions import farms, factories, mines
    farmsClass = farms.farm()
    global users
    for person in users:
        if name == person.name:
            print("Signed in as " + str(person.name))
            #printVars(person)
            #Button detection below
            if True:
                #Finances.html -------------#
                #Farms ---------------------#
                if 'sellFarm' in request.form:
                    print("Detected 'sellFarm'")

                elif 'buyFarm' in request.form:
                    print("Detected 'buyFarm'")
                    if hasMoney(person, farmsClass.farmCost):
                        person.numberFarms += 1
                        person.money -= farmsClass.farmCost
                        print("Brought one farm")
                    else:
                        print("Money Error: Not enough money")


                elif 'upgradeFarm' in request.form:
                    print("Detected 'upgradeFarm'")
                    if person.farmLevel >= 5:
                        print("Error: Max farm level")
                    else:
                        if hasMoney(person, farmsClass.levelCost):
                            person.farmLevel += 1
                            person.money -= farmsClass.levelCost
                            print("Upgraded Level")
                        else:
                            print("Money Error: Not enough money")

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

            #Save personal Data
            print('Saving...')
            username = person.name + '.p'
            fname = os.path.join(PICKLE_DIR, username)
            with open(fname, 'wb') as f:
                pickle.dump(person, f)


    print("Redirect")
    return redirect(url_for('user', name=name))

if __name__ == "__main__":
    #app.run()
    app.run('0.0.0.0', 8080)
    #hi
