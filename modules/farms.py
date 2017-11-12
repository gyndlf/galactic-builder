# The code to calculate the farms. This is not done for each specific user.
# Used to calculate farm costing and level costs

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def farm(values, totals):
    """The farms calculation. Calculates all the formulas for farms"""
    logger.info('[3] Running farms def')

    population = values.population
    foodNeeded = population * 2
    foodSent = totals['foodSent']
    farmValue = (foodNeeded - foodSent) * 2
    farmCost = farmValue * 20
    levelCost = farmCost * 50

    calculated = {
        'foodNeeded': foodNeeded,
        'foodSent': foodSent,
        'farmValue': farmValue,  # Selling food value (price food sells at)
        'farmCost': farmCost,
        'levelCost': levelCost
    }
    return calculated
