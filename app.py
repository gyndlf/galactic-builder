# This is the main python file.
# Please do not touch unless your are ABSOLUTELY SURE ABOUT WHAT YOU ARE DOING
# Thanks :)

# export FLASK_APP=mainpythonfile.py
# python -m flask run

import pickle
import os, sys
from flask import *
import string as s

app = Flask(__name__)

message = ""
number = 0

CHAR_SET = s.printable[:-5]  # All valid characters
SUBSTITUTION_CHARS = CHAR_SET[-3:] + CHAR_SET[:-3]  # Moves them over by 3

#Create the encryption and decryption dictionaries
ENCRYPT_DICT = {}
DECRYPT_DICT = {}
for i,c in enumerate(CHAR_SET):
    v = SUBSTITUTION_CHARS[i]
    ENCRYPT_DICT[c] = v
    DECRYPT_DICT[v] = c

# Calculate file paths
MY_DIR = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')
USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)
DATABASE = 'database.p'
DATABASEPATH = os.path.join(PICKLE_DIR, DATABASE)
VALUES = 'values.p'
VALUESPATH = os.path.join(PICKLE_DIR, VALUES)


def printVars(object):
    print(str(object) + " vars: " + str(vars(object)))


def loadUsers():
    print('[1] Loading users')
    users = []
    # Load users from their .p files
    with open(USERSPATH, 'rb') as f:
        usersArray = pickle.load(f)

    for file in usersArray:
        fname = os.path.join(PICKLE_DIR, file)
        # print("Opening " + str(fname))
        with open(fname, 'rb') as f:
            peps = pickle.load(f)
            users.append(peps)
    return users


def loadValues():
    print('[1] Load values')
    with open(VALUESPATH, 'rb') as f:
        values = pickle.load(f)
    return values

def scrambleCookie (request, username):
    #Scrambles the cookies!!!!
    text = []
    for i in username:
        v = ENCRYPT_DICT[i]
        text.append(v)
    cookie = ''.join(text)
    request.set_cookie('sessionID', cookie)
    return request


def loadCookie(username):
    # Converts the cypher to words.
    text = []
    for i in username:
        v = DECRYPT_DICT[i]
        text.append(v)
    return ''.join(text)

def hasMoney(object, money):
    try:
        if object.money >= money:
            return True
        else:
            return False
    except:
        return False


def total(users):
    # These are things like total food sent, total net worth
    print('[2] Running total definition')

    foodSent = 0
    totalMoney = 0
    totalMines = 0

    for person in users:
        foodSent += person.foodProduced
        totalMoney += person.money
        for mine in person.ownedMines:
            totalMines += person.ownedMines[mine]

    #print('Total mines ' + str(totalMines))
    calculated = {
        'foodSent': foodSent,
        'totalMoney': totalMoney,
        'totalMines': totalMines
    }

    # print("Total food sent " + str(foodSent))
    # print("Total money in the game " + str(totalMoney))

    return calculated


def farm(users, values, totals):
    print('[3] Running farms def')
    # All farm calculations done here. Not farms.py

    population = values.population
    foodNeeded = population * 2
    foodSent = totals['foodSent']
    farmValue = (foodNeeded - foodSent) * 2
    farmCost = farmValue * 20
    levelCost = farmCost * 50

    calculated = {
        'foodNeeded': foodNeeded,
        'foodSent': foodSent,
        'farmValue': farmValue,  # Selling farm cost
        'farmCost': farmCost,
        'levelCost': levelCost
    }
    return calculated


def mine(values, totals):
    # The mine calculations
    print('[3] Running mine def')
    calculated = {}

    for mine in values.mineValues:
        mineCost = totals['totalMines'] * values.mineValues[mine]
        if mineCost < 1200:
            mineCost = 1200
        print('Mine cost: ', mine, mineCost)
        calculated[mine] = mineCost
    # Number of mines
    # amount produced = number of mines * percentage boost
    # mine cost = total mines * mine value
    #print(calculated)
    return calculated


def factory():
    # The factory calculations
    print('[3] Running factory def')
    users = loadUsers()
    values = loadValues()
    totals = total()

    calculated = {
        'nothing': None
    }

    # productCost = 0
    # factoryLevel = 1
    # amountProduced = 2^factoryLevel*2
    # income = productCost * amountProduced
    # upgrade = income * 5
    # materialCost = 0 #Changed in other classes
    # profit = income - (materialCost * amountProduced)
    return calculated


def dynamicPersonalCalc(object, farms, mines, values):
    # Calculate personal dynamic varibles
    print('[4] Running dynamic personal calulator def')


    # Farms
    Fproduced = object.farmLevel * object.numberFarms
    Fincome = Fproduced * farms['farmValue']

    # Mines
    minesDict = {}
    for name in values.mineValues:
        produced = object.ownedMines[name] * object.mineBoost
        minesDict[name] = produced

    income = Fincome + 0  # Add factory income and mine income here
    expenses = int(income / 5)  # (Tax) Add all expenses here
    netIncome = income - expenses

    calculated = {
        'Fproduced': Fproduced,
        'Fincome': Fincome,
        'income': income,
        'expenses': expenses,
        'netIncome': netIncome,
        'minesDict' : minesDict
    }
    # Input new varibles into "object" object
    object.foodProduced = Fproduced
    object.income = income
    object.expenses = expenses
    object.netIncome = netIncome
    object.mineProduced = minesDict
    print('Dynamic personal number of mines: ', minesDict)

    # Save new varibles to file
    username = object.name + '.p'
    fname = os.path.join(PICKLE_DIR, username)
    print("[-] Saving dynamic personal data to " + str(username))
    with open(fname, 'wb') as f:
        pickle.dump(object, f)

    return calculated


# All app.route functions --------------#
@app.route('/')
def home():
    # The login page
    #return redirect(url_for('user', name='james', page='home'))  # A little hotwire for debuging
    return render_template('index.html')


@app.route('/loginuser', methods=['POST'])
def calcmessage():
    # The script that runs once you login
    users = loadUsers()
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        return redirect(url_for('home'))
    for person in users:
        if person.name == username and person.password == password:
            print("Logging in to " + str(username))
            resp = make_response(redirect(url_for('user', name=username, page='home')))
            print("Saving cookie 'sessionID'")
            resp = scrambleCookie(resp, username)
            return resp
    return redirect(url_for('home'))

@app.route('/user/')
@app.route('/user/<name>')
@app.route('/user/<name>/<page>')
def user(name=None, page=None):
    print("-" * 10 + str("Finances") + "-" * 10)

    try: #Load the session cookie
        cookie = request.cookies.get('sessionID')
        print('Username via cookie: ', cookie)
    except:
        return 'No cookie found.'

    cookie = loadCookie(cookie)

    if cookie != name:
        return 'You do not have access to this location'

    #Calculate the very basics
    values = loadValues()
    users = loadUsers()
    totals = total(users)

    # Calculate the recipies
    print('Calculating dynamic varibles...')
    farms = farm(users, values, totals)
    mines = mine(values, totals)
    # factories = factory()

    # Identify the user
    for person in users:
        if name == person.name:
            # Calculate dynamic personal varibles
            print('Calculating dynamic personal varibles')
            dynamicPersonal = dynamicPersonalCalc(person, farms, mines, values)

            # Test it
            print('[] Personal income $' + str(dynamicPersonal['income']))
            print('[] Everyone is sending ' + str(totals['foodSent']) + ' bits of food.')

            # Return the html
            if page == 'home':
                print("Rendering home html...")
                return render_template('finances.html', username=person.name, money=person.money,
                                       netIncome=person.netIncome,
                                       income=person.income, expenses=person.expenses, netWorth=0)

            elif page == 'farms':
                print('Rendering farm html...')
                return render_template('farms.html', username=person.name, farmIncome=dynamicPersonal['Fincome'],
                                       numOfFarms=person.numberFarms,
                                       amountProduced=dynamicPersonal['Fproduced'],
                                       farmCost=farms['farmCost'], farmLevel=person.farmLevel,
                                       farmLevelCost=farms['levelCost'], farmValue=farms['farmValue'],
                                       population=values.population,
                                       foodProduced=dynamicPersonal['Fproduced'])

            elif page == 'mines':
                print('Rendering mines html...')
                templateData = {
                    'minesFunc': mines,
                    'dynamicPersonal' : dynamicPersonal,
                    'values' : values,
                    'person' : person
                }
                return render_template('mines.html', username=person.name, **templateData)

            elif page == 'factories':
                print("Rendering factories html...")
                return render_template('factories.html', username=person.name)

            elif page == 'community':
                print("Rendering community html..")
                return render_template('community.html', username=person.name)

            else:
                return "Invalid page name"
    return "Invaild username"


@app.route('/user/<name>/button', methods=['POST'])
def userButton(name=None):
    print("-" * 10 + str("Button") + "-" * 10)

    # Run recipies
    users = loadUsers()
    values = loadValues()
    totals = total(users)
    print("Loading recipies...")
    farms = farm(users, values, totals)
    # Load users

    farmHtml = False
    mineHtml = False

    for person in users:
        if name == person.name:
            print("Signed in as " + str(person.name))
            # Button detection below

            # farms.html -------------#
            if 'buyFarm' in request.form:
                print("Detected 'buyFarm'")
                farmHtml = True
                if hasMoney(person, farms['farmCost']):
                    person.numberFarms += 1
                    person.money -= farms['farmCost']
                    print("Brought one farm")
                else:
                    print("Money Error: Not enough money")


            elif 'upgradeFarm' in request.form:
                print("Detected 'upgradeFarm'")
                farmHtml = True
                if person.farmLevel >= 5:
                    print("Error: Max farm level")
                else:
                    if hasMoney(person, farms['levelCost']):
                        person.farmLevel += 1
                        person.money -= farms['levelCost']
                        print("Upgraded Level")
                    else:
                        print("Money Error: Not enough money")

            # Factories -----------------#

                # Mines --------------------#
            elif 'buymine1' in request.form:
                print("Detected 'buymine1'")
                mineHtml = True

            elif 'buymine2' in request.form:
                print("Detected 'buymine2'")
                mineHtml = True

            elif 'buymine3' in request.form:
                print("Detected 'buymine3'")
                mineHtml = True

            else:
                print('Unknown value')

                    # Save personal Data
            print('Saving...')
            username = person.name + '.p'
            fname = os.path.join(PICKLE_DIR, username)
            with open(fname, 'wb') as f:
                pickle.dump(person, f)

    print("Calculating redirect")
    if farmHtml:
        print('Redirecting back to farms')
        return redirect(url_for('user', name=name, page='farms'))
    elif mineHtml:
        print('Redirecting back to mines')
        return redirect(url_for('user', name=name, page='mines'))
    else:
        print('Redirecting to home')
        return redirect(url_for('user', name=name, page='home'))


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
    #app.run('0.0.0.0', 8080)
