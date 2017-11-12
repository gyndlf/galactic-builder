import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def total(users, values):
    """Calculate totals across all the users"""
    logger.info('[2] Running total definition')

    foodSent = 0  # The total food created by all the players
    totalMoney = 0  # The total money in circulation in the game
    totalMines = 0  # The total count of mines in the game
    avgWealth = 0  # Average wealth of all the payers (currently not used)
    wealth = {}  # Lookup dictionary of a person's wealth
    factories = {}  # Lookup dictionary of each factories count
    for factoryh in values.factoryValues:
        factories[factoryh] = 0

    # Add them all up!
    for person in users:
        foodSent += person.foodProduced
        totalMoney += person.money
        wealth[person.name] = int(person.netIncome * random.randint(7500, 12500) / 10000)
        message = str(person.name) + "'s wealth " + str(wealth[person.name])
        logger.debug(message)
        for mine in person.ownedMines:
            totalMines += person.ownedMines[mine]
        for factoryh in person.ownedFactories:
            factories[factoryh] += person.ownedFactories[factoryh]

    count = 0
    for item in wealth:
        avgWealth += wealth[item]
        count += 1
    avgWealth = int(round((avgWealth / count), 0))

    # Put them in a dictionary
    calculated = {
        'foodSent': foodSent,
        'totalMoney': totalMoney,
        'totalMines': totalMines,
        'factoryCount': factories,
        'wealth': wealth,
        'avgWealth': avgWealth
    }
    logger.debug('Calculated factory count %s', factories)
    return calculated


if __name__ == '__main__':  # The file is run directly
    print('Error 321: Unknown values')
