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
        self.foodNeeded = self.population*2
        self.foodSent = values.foodSent
        self.farmValue = (self.foodNeeded - self.foodSent)*2

        self.farmCost = self.farmValue * 20
        self.levelCost = self.farmCost * 50