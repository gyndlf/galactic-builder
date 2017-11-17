# This is the main python file.
# Please do not touch unless your are ABSOLUTELY SURE ABOUT WHAT YOU ARE DOING
# Thanks :)
# https://pythonspot.com/en/flask-and-great-looking-charts-using-chart-js/

# export FLASK_APP=mainpythonfile.py
# python -m flask run

WHICH_DATABASE = 'pickle'  # Or can be 'google'
ENABLE_TEST = False

import pickle
import os
from flask import *
import logging

# Import the modules needed to calculate everything
from modules import general, total, farms, mines, factories, DPC

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

app = Flask(__name__)

# Create the encryption and decryption dictionaries
seed = 21904867982759875983275982375893
logger.info('The seed is %s', seed)
ENCRYPT_DICT, DECRYPT_DICT = general.randomchars(seed)

# Calculate file paths
MY_DIR = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')
USERS = "users.p"
USERS_PATH = os.path.join(PICKLE_DIR, USERS)
DATABASE = 'database.p'
DATABASE_PATH = os.path.join(PICKLE_DIR, DATABASE)
VALUES = 'values.p'
VALUES_PATH = os.path.join(PICKLE_DIR, VALUES)


if WHICH_DATABASE is 'pickle':
    from modules import pickledata
elif WHICH_DATABASE is 'google':
    pass
else:
    logger.error('CRITICAL ERROR: Unknown database')
    quit()

if ENABLE_TEST:
    # Before doing anything important, first make sure that all of the varibles are similar across the board
    # Check if each person has the same as the database.py and database.p files
    # Is not perfect as it cannot check the one varibles, only lists.
    # Can be disabled by the ENABLE_TEST boolean

    u = pickledata.loadusers(USERS_PATH, PICKLE_DIR)
    v = pickledata.loadvalues(VALUES_PATH)

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
else:
    logger.warning('Warning: Not running the cross reference varible test')


# All app.route functions -----------------------------------------------------------------------------------------#
@app.route('/')
def home():
    """The main login page / Index"""
    return render_template('index.html')


@app.route('/loginuser', methods=['POST'])
def calcmessage():
    """This is the login script"""
    if WHICH_DATABASE is 'pickle':
        users = pickledata.loadusers(USERS_PATH, PICKLE_DIR)
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
    elif WHICH_DATABASE is 'google':
        logger.warning('Google database not migrated')
        return 'Not migrated get.'
    else:
        logger.error('Error: No database set')
        return 'Error: Database not set'


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
    if data:
        dialogMessage = data
    else:
        dialogMessage = None

    if WHICH_DATABASE is 'pickle':

        # Calculate the very basics
        values = pickledata.loadvalues(VALUES_PATH)
        users = pickledata.loadusers(USERS_PATH, PICKLE_DIR)
        totals = total.total(users, values)

        # Calculate the recipies
        logger.info('Calculating dynamic varibles...')
        farm = farms.farm(values, totals)
        minecalcd = mines.mine(values, totals)
        factory = factories.factory(values, totals)

        # Identify the user
        for person in users:
            if name == person.name:  # Name is from the url
                # Calculate dynamic personal varibles
                dynamicPersonal = DPC.dynamicPersonalCalc(person, farm, values, PICKLE_DIR)

                templateData = {
                    'minesFunc': minecalcd,
                    'dialogMessage': dialogMessage,
                    'dynamicPersonal': dynamicPersonal,
                    'values': values,
                    'person': person,
                    'totals': totals,
                    'factories': factory,
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

                elif page == 'settings':
                    logger.info('Rendering settings html')
                    return render_template('settings.html', **templateData)

                else:
                    logger.error('Invalid page name!')
                    return "Invalid page name"
        logger.error('Invalid username!')
        return "Invaild username"
    elif WHICH_DATABASE is 'google':
        logger.warning('Google database not migrated')
        return 'Not migrated get.'
    else:
        logger.error('Error: No database set')
        return 'Error: Database not set'


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

    if WHICH_DATABASE is 'pickle':
        # Run recipies. Because other users could be online and you want to be upto date
        logger.info("Loading recipies...")
        users = pickledata.loadusers(USERS_PATH, PICKLE_DIR)
        values = pickledata.loadvalues(VALUES_PATH)
        totals = total.total(users, values)
        farm = farms.farm(values, totals)
        minecalcd = mines.mine(values, totals)
        factory = factories.factory(values, totals)

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
                        error = 'Not Enough Money!'

                elif 'upgradeFarm' in request.form:
                    logger.info("Detected 'upgradeFarm'")
                    farmHtml = True
                    if person.farmLevel >= 5:
                        logger.error("Error: Max farm level")
                        error = 'At max farm level of 5. Cannot advance'
                    else:
                        if general.hasmoney(person, farm['levelCost']):
                            person.farmLevel += 1
                            person.money -= farm['levelCost']
                            logger.info("Upgraded Level")
                        else:
                            logger.error("Money Error: Not enough money")
                            error = 'Not Enough Money!'
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
                        error = 'Not Enough Money!'

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
                                error = 'Not Enough Money!'
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
                                error = 'Not Enough Money!'
                    # Factories
                    for factoryl in person.ownedFactories:
                        button = 'buy' + factoryl
                        if button in request.form:
                            logger.info('Factory detected')
                            factoryHtml = True
                            if general.hasmoney(person, factory[factoryl]):
                                person.ownedFactories[factoryl] += 1
                                person.money -= factory[factoryl]
                                logger.info('Brought one %s factory', factoryl)
                            else:
                                logger.error("Money Error: Not enough money")
                                error = 'Not Enough Money!'

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
                                error = 'Not Enough Money!'
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
    elif WHICH_DATABASE is 'google':
        logger.warning('Google database not migrated')
        return 'Not migrated get.'
    else:
        logger.error('Error: No database set')
        return 'Error: Database not set'


@app.route('/testing')
def testing():
    data = 'This is data sent from Python to Javascript'
    return render_template("newFinances.html", person=person)


if __name__ == "__main__":
    # app.run(debug=True)
    logger.info('Running app')
    app.run()
    # app.run('0.0.0.0', 80)
