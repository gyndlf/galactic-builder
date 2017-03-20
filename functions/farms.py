#Functions for farms

import pickle, os, sys

MY_DIR  = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
PICKLE_DIR = os.path.join(MY_DIR, 'data')
VALUES = 'values.p'
VALUESPATH = os.path.join(PICKLE_DIR, VALUES)

with open(VALUESPATH, 'rb') as f:
    values = pickle.load(f)

class farm ():
    def __init__(self):
        self.population = values.population
        self.foodNeeded = self.population*5
        self.foodSent = values.foodSent
        self.sellFoodValue = (self.foodNeeded - self.foodSent)*3

        #Need to change
        self.farmValue = int(self.sellFoodValue/10)

        self.farmCost = self.farmValue * 3000
        self.levelCost = self.farmCost * 500