#Stores base values like farm values and upgrade cost

#No formulas in here!

class basic ():
    def __init__(self):
        #Mines
        #self.steelMineValue = 1341
        #self.noobMineValue = 985
        self.mineValues = {
        	'steel' : 100,
        	'hydrogen' : 50,
        	'titanium' : 250,
            'yellow_crystal': 1000,
            'white_crystal': 500,
            'diamond': 750,
            'silicon': 50,
            'copper': 100,
            'noobidium': 1,
            'helium': 100
        }

        self.factoryValues = {
            'Car' : 30000, #10 steel, 1 silicon,
            'xPhone' : 1000, #2 titianium, 1 copper, 1 silicon (Possible weapon license)
            'AppyLyinx' : 2000, #5 titianium, 3 copper, 3 silicon, 1 noobidium
            'Toilet' : 50, #10 noobidium
            'Pii Fighter' : 100000, #50 steel, 20 titianium, 10 hydrogen, 1 white crystal, weapon lisence core, fighter license
            '4d Printer' : 200000 #10 steel, 10 copper, 10 silicon, 1 white crystal, 1 yellow crystal
        }

        #Farms
        self.population = 200
