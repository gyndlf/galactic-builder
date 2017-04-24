# This is the main python file.
# Please do not touch unless your are ABSOLUTELY SURE ABOUT WHAT YOU ARE DOING
# Thanks :)
# https://pythonspot.com/en/flask-and-great-looking-charts-using-chart-js/

# export FLASK_APP=mainpythonfile.py
# python -m flask run

import pickle
import os, sys
from flask import *
import string as s
import random
import math
import logging

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler('logs.log')
handler.setFormatter(formatter)

logger = logging.getLogger('')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

seed = 943787649038648697347696748967943
random.seed(seed)
logger.info('The seed is %s', seed)
app = Flask(__name__)

CHAR_SET = s.printable[:-5]  # All valid characters
logger.info('All characters %s', CHAR_SET)
CHAR_SET = CHAR_SET.replace("\\", "")  # Remove backslash
CHAR_SET = CHAR_SET.replace("'", '')  # Remove single quote
CHAR_SET = CHAR_SET.replace('"', '')  # Remove double quote
CHAR_SET = CHAR_SET.replace(',', '')  # Remove commar
CHAR_SET = CHAR_SET.replace('`', '')  # Remove thingy
word = list(CHAR_SET)
logger.info('Valid character %s', CHAR_SET)
random.shuffle(word)
CHAR_SET = ''.join(word)
logger.info('Shuffled characters %s', CHAR_SET)
SUBSTITUTION_CHARS = CHAR_SET[-3:] + CHAR_SET[:-3]  # Moves them over by 3

# Create the encryption and decryption dictionaries
ENCRYPT_DICT = {}
DECRYPT_DICT = {}

for i, c in enumerate(CHAR_SET):
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


def loadUsers():
    '''Load users from the file given as USERS'''
    logger.info('[1] Loading users')
    users = []
    # Load users.p files
    with open(USERSPATH, 'rb') as f:
        usersArray = pickle.load(f)

    # Read to find out the users
    for file in usersArray:
        fname = os.path.join(PICKLE_DIR, file)
        with open(fname, 'rb') as f:
            person = pickle.load(f)
            users.append(person)
    return users


def loadValues():
    '''Load the values from the file given as VALUES'''
    logger.info('[1] Load values')
    with open(VALUESPATH, 'rb') as f:
        values = pickle.load(f)
    return values


def scrambleCookie(request, username):
    '''Scramble the username and add to the give request'''
    t = []
    for i in username:
        v = ENCRYPT_DICT[i]
        t.append(v)
    sessio = ''.join(t)
    request.set_cookie('sessionID', sessio)
    return request


def loadCookie(username):
    '''Decrypt the username'''
    # Converts the cypher to words.
    h = []
    for i in username:
        v = DECRYPT_DICT[i]
        h.append(v)
    return ''.join(h)


def hasMoney(object, money):
    '''Weather or not the object has >= money'''
    try:
        if object.money >= money:
            return True
        else:
            return False
    except:
        return False


def total(users, values):
    '''Calculate totals across all the users'''
    logger.info('[2] Running total definition')

    foodSent = 0
    totalMoney = 0
    totalMines = 0
    wealth = {}
    factories = {}
    for factoryh in values.factoryValues:
        factories[factoryh] = 0

    # Add them all up!
    for person in users:
        foodSent += person.foodProduced
        totalMoney += person.money
        tmpWealth = person.netIncome * int(math.sqrt(person.money))
        if tmpWealth < 1:
            tmpWealth = 0
        wealth[person.name] = tmpWealth
        message = str(person.name) + "'s wealth " + str(wealth[person.name])
        logger.debug(message)
        for mine in person.ownedMines:
            totalMines += person.ownedMines[mine]
        for factoryh in person.ownedFactories:
            factories[factoryh] += person.ownedFactories[factoryh]

    # Put them in a dictionary
    calculated = {
        'foodSent': foodSent,
        'totalMoney': totalMoney,
        'totalMines': totalMines,
        'factoryCount': factories,
        'wealth': wealth
    }
    logger.debug('Calculated factory count %s', factories)
    return calculated


def farm(values, totals):
    '''The farms calculation. Calculates all the formulas for farms'''
    logger.info('[3] Running farms def')
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
        'farmValue': farmValue,  # Selling food value
        'farmCost': farmCost,
        'levelCost': levelCost
    }
    return calculated


def mine(values, totals):
    '''Calculate the mine costs'''
    logger.info('[3] Running mine def')
    calculated = {}
    # For each mine calculate its costs
    for mine in values.mineValues:
        mineCost = totals['totalMines'] * values.mineValues[mine]  # Number of mines * value of mine
        if mineCost < 1200:
            mineCost = 1200
        msg = 'Mine cost: (' + str(totals['totalMines']) + ' * ' + str(values.mineValues[mine]) + ') ' + str(
            mine) + str(mineCost)
        logger.debug(msg)
        calculated[mine] = mineCost
    return calculated


def factory(values, totals):
    '''Calculate factory costs. Uncompleted.'''

    ''' respourceDisplay = 
    for mine in values.mineValues:
    resourceObject = int(float(str(resources)[:mine]))
    if resourceObject > 0:
    resourceDisplay += mine.value + ":"(mine.total * resourceObject) ","
    resourcecost += mine.total * resourceObject
    return resourceDisplay, '''

    logger.info('[3] Running factory def')

    calculated = {}

    for factoryt in values.factoryValues:
        calculated[factoryt] = values.factoryValues[factoryt] * totals['factoryCount'][factoryt] * 2
        if calculated[factoryt] < 1000:
            calculated[factoryt] = 999
    logger.debug('Calculated factory cost %s', calculated)
    # productCost = 0
    # factoryLevel = 1
    # amountProduced = 2^factoryLevel*2
    # income = productCost * amountProduced
    # upgrade = income * 5
    # materialCost = 0 #Changed in other classes
    # profit = income - (materialCost * amountProduced)
    return calculated


def dynamicPersonalCalc(object, farms, values):
    '''Calculate personal dynamic varibles'''
    logger.info('[4] Running dynamic personal calulator def')

    # Farms
    Fproduced = object.farmLevel * object.numberFarms
    Fincome = Fproduced * farms['farmValue']

    # Mines
    minesDict = {}
    # amount produced = number of mines * percentage boost || Eventually use this
    for name in values.mineValues:
        produced = object.ownedMines[name] * object.mineBoost
        minesDict[name] = produced

    # Factories
    factoryDict = {}
    totalFacIncome = 0
    # amountProduced = numberOfFactories * Bonus(edited)
    # income = productCost * amountProduced
    # profit = income - (materialCost * amountProduced)
    for factoryp in values.factoryValues:
        facProduced = object.ownedFactories[factoryp] * 1  # Add bonus instead of 1 eventually
        facIncome = values.factoryValues[factoryp] * facProduced
        facProfit = facIncome - 0  # Need to add materials next
        totalFacIncome += facProfit
        tmp = {
            'produced': facProduced,
            'income': facIncome,
            'profit': facProfit
        }
        factoryDict[factoryp] = tmp

    # General
    income = Fincome + totalFacIncome  # Add factory income and mine income here
    expenses = int(income / 5)  # (Tax) Add all expenses here
    netIncome = income - expenses

    # Chuck in a dictionary
    calculated = {
        'Fproduced': Fproduced,
        'Fincome': Fincome,
        'income': income,
        'expenses': expenses,
        'netIncome': netIncome,
        'minesDict': minesDict,
        'factories': factoryDict
    }
    # Input new varibles into "object" object
    object.foodProduced = Fproduced
    object.income = income
    object.expenses = expenses
    object.netIncome = netIncome
    object.mineProduced = minesDict
    object.saveFactories = factoryDict
    logger.debug('Dynamic personal number of mines: %s', minesDict)

    # Save new varibles to file
    username = object.name + '.p'
    fname = os.path.join(PICKLE_DIR, username)
    logger.debug("[-] Saving dynamic personal data to %s", str(username))
    with open(fname, 'wb') as f:
        pickle.dump(object, f)
    return calculated


# All app.route functions -----------------------------------------------------------------------------------------#
@app.route('/')
def home():
    '''The main login page / Index'''
    # return redirect(url_for('user', name='james', page='home'))  # A little hotwire for debuging
    return render_template('index.html')


@app.route('/loginuser', methods=['POST'])
def calcmessage():
    '''This is the login script'''
    users = loadUsers()
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        logger.error('Invalid username or password')
        return redirect(url_for('home'))
    for person in users:
        if person.name == username and person.password == password:
            logger.info("Logging in to %s", str(username))
            resp = make_response(redirect(url_for('user', name=username, page='home')))
            logger.debug("Saving cookie 'sessionID'")
            resp = scrambleCookie(resp, username)
            return resp
    logger.error('Username or password does not match database')
    return redirect(url_for('home'))


@app.route('/user/')
@app.route('/user/<name>')
@app.route('/user/<name>/<page>')
def user(name=None, page=None):
    '''The main script. Run whenever logged in'''
    logger.info("-" * 10 + str("Finances") + "-" * 10)

    try:  # Load the session cookie
        cookie = request.cookies.get('sessionID')
        logger.debug('Username via cookie: %s', cookie)
    except:
        logger.error('No cookie found')
        return redirect(url_for('home'))

    cookie = loadCookie(cookie)
    if cookie != name:
        logger.error('Cookie is not the same as %s', name)
        return 'You do not have access to this location'

    # Calculate the very basics
    values = loadValues()
    users = loadUsers()
    totals = total(users, values)

    # Calculate the recipies
    logger.info('Calculating dynamic varibles...')
    farms = farm(values, totals)
    mines = mine(values, totals)
    factories = factory(values, totals)

    # Identify the user
    for person in users:
        if name == person.name:
            # Calculate dynamic personal varibles
            dynamicPersonal = dynamicPersonalCalc(person, farms, values)

            # Return the html
            if page == 'home':
                logger.info("Rendering home html...")  # Need to upgrade to send the whole person
                return render_template('finances.html', username=person.name, money=person.money,
                                       netIncome=person.netIncome,
                                       income=person.income, expenses=person.expenses,
                                       netWorth=totals['wealth'][person.name])

            elif page == 'farms':
                logger.info('Rendering farm html...')  # Use dictionaries below in the future
                return render_template('farms.html', username=person.name, farmIncome=dynamicPersonal['Fincome'],
                                       numOfFarms=person.numberFarms,
                                       amountProduced=dynamicPersonal['Fproduced'],
                                       farmCost=farms['farmCost'], farmLevel=person.farmLevel,
                                       farmLevelCost=farms['levelCost'], farmValue=farms['farmValue'],
                                       population=values.population,
                                       foodProduced=dynamicPersonal['Fproduced'])

            elif page == 'mines':
                logger.info('Rendering mines html...')
                templateData = {
                    'minesFunc': mines,
                    'dynamicPersonal': dynamicPersonal,
                    'values': values,
                    'person': person
                }
                return render_template('mines.html', username=person.name, **templateData)

            elif page == 'factories':
                logger.info("Rendering factories html...")
                templateData = {
                    'formulas': dynamicPersonal['factories'],
                    'cost': factories,
                    'person': person,
                    'totals': totals
                }
                return render_template('factories.html', username=person.name, **templateData)

            elif page == 'community':
                logger.info("Rendering community html..")
                labels = []
                info = []
                data = totals['wealth']
                for item in data:
                    info.append(data[item])
                    labels.append(item)
                colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD"]
                return render_template('community.html', username=person.name, set=zip(info, labels, colors))

            elif page == 'species':
                logger.info('Rendering species html')
                return render_template('species.html', username=person.name)

            else:
                logger.error('Invalid page name!')
                return "Invalid page name"
    logger.error('Invalid username!')
    return "Invaild username"


@app.route('/user/<name>/button', methods=['POST'])
def userButton(name=None):
    '''The script runs once ANY button is pressed'''
    logger.info("-" * 10 + str("Button") + "-" * 10)

    try:  # Load the session cookie
        cookie = request.cookies.get('sessionID')
        logger.debug('Username via cookie: %s', cookie)
    except:
        logger.error('No cookie found')
        return 'No cookie found.'

    cookie = loadCookie(cookie)
    if cookie != name:
        logger.error('Cookie does not match database')
        return 'You do not have access to this location'

    # Run recipies
    logger.info("Loading recipies...")
    users = loadUsers()
    values = loadValues()
    totals = total(users, values)
    farms = farm(values, totals)
    mines = mine(values, totals)
    factories = factory(values, totals)

    farmHtml = False
    mineHtml = False
    factoryHtml = False

    # Identify the user
    for person in users:
        if name == person.name:
            logger.info("Signed in as " + str(person.name))

            # Detect what button it was and do the appropriate action

            # farms.html ---------------#
            if 'buyFarm' in request.form:
                logger.info("Detected 'buyFarm'")
                farmHtml = True
                if hasMoney(person, farms['farmCost']):
                    person.numberFarms += 1
                    person.money -= farms['farmCost']
                    logger.info("Brought one farm")
                else:
                    logger.error("Money Error: Not enough money")

            elif 'upgradeFarm' in request.form:
                logger.info("Detected 'upgradeFarm'")
                farmHtml = True
                if person.farmLevel >= 5:
                    logger.error("Error: Max farm level")
                else:
                    if hasMoney(person, farms['levelCost']):
                        person.farmLevel += 1
                        person.money -= farms['levelCost']
                        logger.info("Upgraded Level")
                    else:
                        logger.error("Money Error: Not enough money")

            # Factories ----------------#

            # Mines --------------------#
            else:
                # Mines
                for digger in person.ownedMines:
                    button = 'buy' + digger
                    if button in request.form:
                        logger.info('Detected mine button')
                        mineHtml = True
                        if hasMoney(person, mines[digger]):
                            person.ownedMines[digger] += 1
                            person.money -= mines[digger]
                            logger.info('Brought one %s mine', digger)
                        else:
                            logger.error("Money Error: Not enough money")
                # Factories
                for factoryl in person.ownedFactories:
                    button = 'buy' + factoryl
                    if button in request.form:
                        logger.info('Factory detected')
                        factoryHtml = True
                        if hasMoney(person, factories[factoryl]):
                            person.ownedFactories[factoryl] += 1
                            person.money -= factories[factoryl]
                            logger.info('Brought one %s factory', factoryl)
                        else:
                            logger.error("Money Error: Not enough money")

            # Save upated personal data
            logger.info('Saving...')
            username = person.name + '.p'
            fname = os.path.join(PICKLE_DIR, username)
            with open(fname, 'wb') as f:
                pickle.dump(person, f)

    # Redirect back to the page the user was at before
    logger.info("Calculating redirect")
    if farmHtml:
        logger.info('Redirecting back to farms')
        return redirect(url_for('user', name=name, page='farms'))
    elif mineHtml:
        logger.info('Redirecting back to mines')
        return redirect(url_for('user', name=name, page='mines'))
    elif factoryHtml:
        logger.info('Redirecting back to factories')
        return redirect(url_for('user', name=name, page='factories'))
    else:
        logger.info('Redirecting to home')
        return redirect(url_for('user', name=name, page='home'))


if __name__ == "__main__":
    # app.run(debug=True)
    logger.info('Running app')
    app.run()
    # app.run('0.0.0.0', 8080)
