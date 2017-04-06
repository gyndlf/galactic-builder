#Stores base values like farm values and upgrade cost

#No formulas in here!

class basic ():
    def __init__(self):
        #Mines
        #self.steelMineValue = 1341
        #self.noobMineValue = 985
        self.mineValues = {
        	'mine1' : 1000,
        	'mine2' : 500,
        	'mine3' : 250
        }


        #Farms
        self.population = 200
