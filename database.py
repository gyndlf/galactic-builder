# Data base file
# So far the script can only read from this file and not update it. That will have to change...

# No formulas in here!!! Cheeky cheeky!

# Anything?


class person:
    def __init__(self):
        # General
        self.name = ""
        self.password = 'password'
        self.id = 0
        self.money = 10000
        self.netWorth = 0
        self.salary = 0
        self.income = 0
        self.expenses = 0
        self.netIncome = 0

        # Farms
        self.numberFarms = 1
        self.farmLevel = 1
        self.foodProduced = 0

        # Mines
        self.ownedMines = {
            'steel': 0,
            'hydrogen': 0,
            'titanium': 0,
            'yellow crystal': 0,
            'white crystal': 0,
            'diamond': 0,
            'silicon': 0,
            'copper': 0,
            'noobidium': 0,
            'helium': 0,
            'gold': 0,
            'liquid nitrogen': 0,
            'carbon fiber': 0,
            'oil': 0,
            'uranium': 0,
            'francium': 0,
            'lead': 0,
            'carbon': 0
        }
        self.ownedFactories = {
            'Car': 0,  # 10 steel, 1 silicon,
            'iPhoneX': 0,  # 2 titianium, 1 copper, 1 silicon (Possible weapon license)
            'AppyLyinx': 0,  # 5 titianium, 3 copper, 3 silicon, 1 noobidium
            'Toilet': 0,  # 10 noobidium
            'Pii Fighter': 0,
            # 50 steel, 20 titianium, 10 hydrogen, 1 white crystal, weapon lisence core, fighter license
            '4d Printer': 0,  # 10 steel, 10 copper, 10 silicon, 1 white crystal, 1 yellow crystal
            'X128 CPU': 0,
            'robot': 0,
            'batteries': 0,
            'plasma compressor': 0,
            'laser': 0,
            'death star': 0
        }
        self.ownedShips = {
            'j10exs': 0,
            'j9exs': 0,
            'j8exs': 0,
            'j7exs': 0,
            'j6exs': 0
        }
        self.mineProduced = {}
        self.saveFactories = {}
        self.totalMines = 0
        self.mineBoost = 1  # Is representing a number/100. So 5 is a 5% bonus.
        self.minePowerUpgrade = 1
