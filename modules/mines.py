# The code to calculate the mines. This is not done for each specific user.
# Used to calculate mine costing and level costs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def mine(values, totals):
    """Calculate the mine costs"""
    logger.info('[3] Running mine def')
    calculated = {}

    # For each mine calculate its costs
    for value in values.mineValues:
        minecost = totals['totalMines'] * values.mineValues[value]  # Number of mines * value of mine
        if minecost < 1200:
            minecost = 1200
        msg = 'Mine cost: (' + str(totals['totalMines']) + ' * ' + str(values.mineValues[value]) + ') ' + str(
            value) + str(minecost)
        logger.debug(msg)
        calculated[value] = minecost

    # Mine upgrades
    base = int(totals['avgWealth'] / 10)
    if base < 100:
        base = 100
    root10 = base * 9
    root50 = base * 45
    root100 = base * 90
    root2 = root100 * root50
    mineUpgrades = {
        1: base,
        10: root10,
        50: root50,
        100: root100,
        2: root2
    }
    calculated['mineUpgrades'] = mineUpgrades
    return calculated


if __name__ == '__main__':  # The file is run directly
    print('Error 321: Unknown values')
