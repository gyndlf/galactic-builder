# The code to calculate the factories. This is not done for each specific user.
# Used to calculate factory costing and level costs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
