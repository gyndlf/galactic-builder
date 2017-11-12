# This is the main python file.
# Please do not touch unless your are ABSOLUTELY SURE ABOUT WHAT YOU ARE DOING
# Thanks :)
# https://pythonspot.com/en/flask-and-great-looking-charts-using-chart-js/

# export FLASK_APP=mainpythonfile.py
# python -m flask run


import pickle
import os
from flask import *
import string as s
import random
import logging

# Import the modules needed to calculate everything
from modules import general, total, farms, mines

import baseValues  # Only used in the inital check to see if everything is in sync
import database  # Only used in the inital check to see if everything is in sync


runingonamazon = False

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler('logs.log')
handler.setFormatter(formatter)

if runingonamazon:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger('')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

seed = 21904867982759875983275982375893
random.seed(seed)
logger.info('The seed is %s', seed)
app = Flask(__name__)

CHAR_SET = s.printable[:-5]  # All valid characters
logger.debug('All characters %s', CHAR_SET)
CHAR_SET = CHAR_SET.replace("\\", "")  # Remove backslash
CHAR_SET = CHAR_SET.replace("'", '')  # Remove single quote
CHAR_SET = CHAR_SET.replace('"', '')  # Remove double quote
CHAR_SET = CHAR_SET.replace(',', '')  # Remove commar
CHAR_SET = CHAR_SET.replace('`', '')  # Remove thingy
word = list(CHAR_SET)
logger.debug('Valid character %s', CHAR_SET)
random.shuffle(word)
CHAR_SET = ''.join(word)
logger.debug('Shuffled characters %s', CHAR_SET)
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
USERS_PATH = os.path.join(PICKLE_DIR, USERS)
DATABASE = 'database.p'
DATABASE_PATH = os.path.join(PICKLE_DIR, DATABASE)
VALUES = 'values.p'
VALUES_PATH = os.path.join(PICKLE_DIR, VALUES)

# Before doing anything important, first make sure that all of the varibles are similar across the board
# Check if each person has the same as the database.py and database.p files
# Is not perfect as it cannot check the one varibles, only lists.
u = general.loadusers(USERS_PATH, PICKLE_DIR)
v = general.loadvalues(VALUES_PATH)

b = baseValues.basic()
d = database.person()

sample = len(d.ownedMines) + len(d.ownedFactories) + len(d.ownedShips)  # number of owned "stuff"

values = len(b.mineValues) + len(b.factoryRecipies) + len(b.factoryValues) + len(b.shipDesc) # Num of value "stuff"
actual = len(v.mineValues) + len(v.factoryRecipies) + len(v.factoryValues) + len(v.shipDesc)
if values is not actual:
    logger.error('CRITICAL ERROR: Values.p does NOT match baseValues.py\nReset database or update the variables')
    quit()

for person in u:
    if (len(person.ownedMines) + len(person.ownedFactories) + len(person.ownedShips)) is not sample:
        logger.error('CRITICAL ERROR: ' + str(person.name) + "'s varibles do NOT match.\nReset database or update"
                                                             "variables")
        quit()
logger.info('Passed the cross reference variable test')


def factory(values, totals):
    """Calculate factory costs"""

    ''' respourceDisplay = 
    for mine in values.mineValues:
    resourceObject = int(float(str(resources)[:mine]))
    if resourceObject > 0:
    resourceDisplay += mine.value + ":"(mine.total * resourceObject) ","
    resourcecost += mine.total * resourceObject
    return resourceDisplay, '''

    logger.info('[3] Running factory def')

    calculated = {}

    # Calculate factory costs
    for factoryt in values.factoryValues:

        # Make sure that the scaling is correct. Now multiplying by 0
        if totals['factoryCount'][factoryt] == 0:
            calculated[factoryt] = values.factoryValues[factoryt] * 2
        else:
            calculated[factoryt] = values.factoryValues[factoryt] * totals['factoryCount'][factoryt] * 2

        # Make sure the cost is not below 10
        if calculated[factoryt] < 10:
            calculated[factoryt] = 10
    logger.debug('Calculated factory cost %s', calculated)

    # Code from the spreadsheet
    # productCost = 0
    # factoryLevel = 1
    # amountProduced = 2^factoryLevel*2
    # income = productCost * amountProduced
    # upgrade = income * 5
    # materialCost = 0 #Changed in other classes
    # profit = income - (materialCost * amountProduced)
    return calculated


def dynamicPersonalCalc(object, farms, values):
    """Calculate personal dynamic varibles"""
    logger.info('[4] Running dynamic personal calulator def')

    # Farms
    Fproduced = object.farmLevel * object.numberFarms
    Fincome = Fproduced * farms['farmValue']

    # Mines
    minesDict = {}
    # amount produced = number of mines * percentage boost || Eventually use this
    # object.mineBoost is representing a number/100. So 5 is a 5% bonus.
    # object.minePowerUpgrade is the one that lets mines produce more than one material
    for name in values.mineValues:
        produced = object.ownedMines[name] * object.minePowerUpgrade
        produced += int(produced * object.mineBoost / 100)
        minesDict[name] = produced

    # Factories
    factoryDict = {}
    totalFacIncome = 0
    materialsNeeded = {}
    for material in values.mineValues:  # Initialise the materials
        materialsNeeded[material] = 0
    # amountProduced = numberOfFactories * Bonus(edited)
    # income = productCost * amountProduced
    # profit = income - (materialCost * amountProduced)
    for factory in values.factoryValues:
        facProduced = object.ownedFactories[factory] * 1  # Add bonus instead of 1 eventually
        facIncome = values.factoryValues[factory] * facProduced
        facProfit = facIncome - 0  # Need to add materials next

        for material in values.factoryRecipies[factory]:  # Find out how many materials are needed
            materialsNeeded[material] += values.factoryRecipies[factory][material] * facProduced
        totalFacIncome += facProfit

        tmp = {
            'produced': facProduced,
            'income': facIncome,
            'profit': facProfit,
            'materialsRequired': values.factoryRecipies[factory]
        }

        factoryDict[factory] = tmp

    logger.debug('Materials needed in total %s', materialsNeeded)
    logger.debug('Materials produced: %s', minesDict)

    # Calculate sales
    # You produce 400 iron in total but only need 324. The excess 76 will be sold.
    # You produce 200 gold but need 253 and so you will buy 53 gold.

    messages = {}
    materialsSelling = {}
    materialsBuying = {}
    materialsTotalCost = 0
    mineProfitMade = 0

    for material in minesDict:
        materialsSelling[material] = 0
        materialsBuying[material] = 0

    for material in values.mineValues:
        needed = materialsNeeded[material] - minesDict[material]
        if needed < 0:  # Greater than §0. Sell the excess
            selling = abs(needed * values.mineValues[material])
            materialsSelling[material] = selling
            mineProfitMade += selling
            messages[material] = 'You have ' + str(abs(needed)) + ' extra. This will be sold for §' + str(selling)
        elif needed > 0:
            buying = needed * values.mineValues[material]
            materialsBuying[material] = buying
            materialsTotalCost += buying
            messages[material] = 'You need ' + str(needed) + ' more. This will be brought for §' + str(buying)
        else:
            messages[material] = 'You produce just the right amount of resources needed. Good job.'

    # General
    income = Fincome + totalFacIncome + mineProfitMade # Add farm income, mines and factory income here
    expenses = int(income / 5) + materialsTotalCost  # (Tax) Add all expenses here
    netIncome = income - expenses

    # Chuck (Norris) it in a dictionary (== Unkillable)
    calculated = {
        'Fproduced': Fproduced,
        'Fincome': Fincome,
        'income': income,
        'expenses': expenses,
        'netIncome': netIncome,
        'minesDict': minesDict,
        'factories': factoryDict,
        'materialsSelling': materialsSelling,
        'materialsBuying': materialsBuying,
        'mineMessages': messages,
        'mineProfitMade': mineProfitMade,
        'materialsTotalCost': materialsTotalCost,
        'totalFacIncome': totalFacIncome
    }

    # Any point having the code below? It's never used
    # Input new dynamic varibles into "object" object
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
    """The main login page / Index"""
    # return redirect(url_for('user', name='james', page='home'))
    # A little hotwire for debuging. Remember to remove cookie stuff
    return render_template('index.html')


@app.route('/loginuser', methods=['POST'])
def calcmessage():
    """This is the login script"""
    users = general.loadusers(USERS_PATH, PICKLE_DIR)
    try:
        username = request.form['username']
        password = request.form['password']
        username = username.lower()
    except:
        logger.error('Invalid username or password')
        return redirect(url_for('home'))
    for person in users:
        if person.name == username and person.password == password:
            logger.info("Logging in to %s", str(username))
            resp = make_response(redirect(url_for('user', name=username, page='home')))
            logger.debug("Saving cookie 'sessionID'")
            resp = general.scramblecookie(resp, username, ENCRYPT_DICT)
            return resp
    logger.error('Username or password does not match database')
    return redirect(url_for('home'))


@app.route('/user/')
@app.route('/user/<name>')
@app.route('/user/<name>/<page>')
@app.route('/user/<name>/<page>/<data>')
def user(name=None, page=None, data=None):
    """The main script. Run whenever a user does anything"""
    logger.info("-" * 10 + str("Finances") + "-" * 10)

    # Make sure the user is allowed to be here!
    try:  # Load the session cookie
        cookie = request.cookies.get('sessionID')
        logger.debug('Username via cookie: %s', cookie)
    except:
        logger.error('No cookie found')
        return redirect(url_for('home'))

    # Check the cookie matches
    cookie = general.loadcookie(cookie, DECRYPT_DICT)
    if cookie != name:
        logger.error('Cookie is not the same as %s', name)
        return 'You do not have access to this location'

    # Have you been sent here with an error? Get ready to display it!
    if data == 'notEnoughMoney':  # Could change to having the string have the sentance shown. Get rid of if/else
        dialogMessage = 'Not enough money!'
    elif data == 'maxFarmLevel':
        dialogMessage = 'The max farm level is 5'
    else:
        dialogMessage = None

    # Calculate the very basics
    values = general.loadvalues(VALUES_PATH)
    users = general.loadusers(USERS_PATH, PICKLE_DIR)
    totals = total.total(users, values)

    # Calculate the recipies
    logger.info('Calculating dynamic varibles...')
    farm = farms.farm(values, totals)
    minecalcd = mines.mine(values, totals)
    factories = factory(values, totals)

    # Identify the user
    for person in users:
        if name == person.name:  # Name is from the url
            # Calculate dynamic personal varibles
            dynamicPersonal = dynamicPersonalCalc(person, farm, values)

            templateData = {
                'minesFunc': minecalcd,
                'dialogMessage': dialogMessage,
                'dynamicPersonal': dynamicPersonal,
                'values': values,
                'person': person,
                'totals': totals,
                'factories': factories,
                'farms': farm
            }

            # Return the html
            if page == 'home':
                logger.info("Rendering home html...")
                return render_template('finances.html', **templateData)

            elif page == 'farms':
                logger.info('Rendering farm html...')
                return render_template('farms.html', **templateData)

            elif page == 'mines':
                logger.info('Rendering mines html...')
                return render_template('mines.html', **templateData)

            elif page == 'factories':
                logger.info("Rendering factories html...")
                return render_template('factories.html', **templateData)

            elif page == 'community':
                logger.info("Rendering community html..")
                labels = []
                info = []
                data = totals['wealth']
                for item in data:
                    info.append(data[item])
                    labels.append(item)
                colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD"]
                return render_template('community.html', **templateData, set=zip(info, labels, colors))

            elif page == 'species':
                logger.info('Rendering species html')
                return render_template('species.html', **templateData)

            elif page == 'war':
                logger.info('Rendering war html')
                return render_template('war.html', **templateData)

            elif page == 'shipBuying':
                logger.info('Rendering shipBuying html')
                return render_template('shipBuying.html', **templateData)

            elif page == 'diplomacy':
                logger.info('Rendering shipBuying html')
                return render_template('diplomacy.html', **templateData)

            else:
                logger.error('Invalid page name!')
                return "Invalid page name"
    logger.error('Invalid username!')
    return "Invaild username"


@app.route('/user/<name>/button', methods=['POST'])
def userButton(name=None):
    """The script runs once ANY button is pressed"""
    logger.info("-" * 10 + str("Button") + "-" * 10)

    try:  # Load the session cookie
        cookie = request.cookies.get('sessionID')
        logger.debug('Username via cookie: %s', cookie)
    except:
        logger.error('No cookie found')
        return 'No cookie found.'

    cookie = general.loadcookie(cookie, DECRYPT_DICT)
    if cookie != name:
        logger.error('Cookie does not match database')
        return 'You do not have access to this location'

    # Run recipies. Because other users could be online and you want to be upto date
    logger.info("Loading recipies...")
    users = general.loadusers(USERS_PATH, PICKLE_DIR)
    values = general.loadvalues(VALUES_PATH)
    totals = total.total(users, values)
    farm = farms.farm(values, totals)
    minecalcd = mines.mine(values, totals)
    factories = factory(values, totals)

    # Where have you come from?
    farmHtml = False
    mineHtml = False
    factoryHtml = False
    shipBuyHtml = False

    # Has there been an error you should know about?
    error = None

    # Identify the user
    for person in users:
        if name == person.name:
            logger.info("Signed in as " + str(person.name))

            # Detect what button it was and do the appropriate action

            # farms.html ---------------#
            if 'buyFarm' in request.form:
                logger.info("Detected 'buyFarm'")
                farmHtml = True
                if general.hasmoney(person, farm['farmCost']):
                    person.numberFarms += 1
                    person.money -= farm['farmCost']
                    logger.info("Brought one farm")
                else:
                    logger.error("Money Error: Not enough money")
                    error = 'notEnoughMoney'

            elif 'upgradeFarm' in request.form:
                logger.info("Detected 'upgradeFarm'")
                farmHtml = True
                if person.farmLevel >= 5:
                    logger.error("Error: Max farm level")
                    error = 'maxFarmLevel'
                else:
                    if general.hasmoney(person, farm['levelCost']):
                        person.farmLevel += 1
                        person.money -= farm['levelCost']
                        logger.info("Upgraded Level")
                    else:
                        logger.error("Money Error: Not enough money")
                        error = 'notEnoughMoney'
            # Mines --------------------#
            elif 'mineUpgrade' in request.form:
                logger.debug('Detected mineUpgrade')
                mineHtml = True
                if general.hasmoney(person, minecalcd['mineUpgrades'][2]):
                    person.minePowerUpgrade += 1
                    person.money -= minecalcd['mineUpgrades'][2]
                    logger.info("Upgraded mine power upgrade brought")
                else:
                    logger.error("Money Error: Not enough money")
                    error = 'notEnoughMoney'

            else:
                mineUpgrades = [1, 10, 50, 100]
                for percent in mineUpgrades:
                    title = 'mineUpgrade' + str(percent)
                    if title in request.form:
                        logger.info('Detected %s', title)
                        mineHtml = True
                        if general.hasmoney(person, minecalcd['mineUpgrades'][percent]):
                            person.mineBoost += percent
                            person.money -= minecalcd['mineUpgrades'][percent]
                            logger.info("Upgraded mine produced")
                        else:
                            logger.error("Money Error: Not enough money")
                            error = 'notEnoughMoney'
                        logger.info('The users mineBoost is now %s', person.mineBoost)
                # Mines
                for digger in person.ownedMines:
                    button = 'buy' + digger
                    if button in request.form:
                        logger.info('Detected mine button')
                        mineHtml = True
                        if general.hasmoney(person, minecalcd[digger]):
                            person.ownedMines[digger] += 1
                            person.money -= minecalcd[digger]
                            logger.info('Brought one %s mine', digger)
                        else:
                            logger.error("Money Error: Not enough money")
                            error = 'notEnoughMoney'
                # Factories
                for factoryl in person.ownedFactories:
                    button = 'buy' + factoryl
                    if button in request.form:
                        logger.info('Factory detected')
                        factoryHtml = True
                        if general.hasmoney(person, factories[factoryl]):
                            person.ownedFactories[factoryl] += 1
                            person.money -= factories[factoryl]
                            logger.info('Brought one %s factory', factoryl)
                        else:
                            logger.error("Money Error: Not enough money")
                            error = 'notEnoughMoney'

                for ship in person.ownedShips:
                    button = 'buy' + ship
                    if button in request.form:
                        logger.info('shipBuy detected')
                        logger.info('Detected %s', ship)
                        shipBuyHtml = True
                        '''
                        if general.hasmoney(person, factories[factoryl]):
                            person.ownedFactories[factoryl] += 1
                            person.money -= factories[factoryl]
                            logger.info('Brought one %s factory', factoryl)
                        else:
                            logger.error("Money Error: Not enough money")
                            error = 'notEnoughMoney'
                        '''

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
        return redirect(url_for('user', name=name, page='farms', data=error))
    elif mineHtml:
        logger.info('Redirecting back to mines')
        return redirect(url_for('user', name=name, page='mines', data=error))
    elif factoryHtml:
        logger.info('Redirecting back to factories')
        return redirect(url_for('user', name=name, page='factories', data=error))
    elif shipBuyHtml:
        logger.info('Redirecting back to shipBuyHtml')
        return redirect(url_for('user', name=name, page='shipBuying', data=error))
    else:
        logger.info('Redirecting to home')
        return redirect(url_for('user', name=name, page='home', data=error))


@app.route('/testing')
def testing():
    data = 'This is data sent from Python to Javascript'
    return render_template("newFinances.html", person=person)


if __name__ == "__main__":
    # app.run(debug=True)
    logger.info('Running app')
    app.run()
    # app.run('0.0.0.0', 80)
