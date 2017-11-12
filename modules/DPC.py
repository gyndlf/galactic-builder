# This is the Dynamic Personal Calculator


# This is a huge project to migrate. Will be awhile before it can happen
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def dynamicPersonalCalc(object, farms, values, pickledir):
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

    # Legacy system of saving the DPC. Not needed as it is always calculated
    # Any point having the code below? It's never used
    # Input new dynamic varibles into "object" object

    # object.foodProduced = Fproduced
    # object.income = income
    # object.expenses = expenses
    # object.netIncome = netIncome
    # object.mineProduced = minesDict
    # object.saveFactories = factoryDict
    # logger.debug('Dynamic personal number of mines: %s', minesDict)
    # Save new varibles to file
    # filename = object.name + '.p'
    # fname = os.path.join(pickledir, filename)
    # logger.debug("[-] Saving dynamic personal data to %s", str(filename))
    # with open(fname, 'wb') as f:
    #     pickle.dump(object, f)

    return calculated
