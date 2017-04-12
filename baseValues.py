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


        #Farms
        self.population = 200
