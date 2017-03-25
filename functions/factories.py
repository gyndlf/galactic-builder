#Has all factory functions
print('Running "factories.py"')
import pickle, os, sys

MY_DIR  = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
PICKLE_DIR = os.path.join(MY_DIR, 'data')
VALUES = 'values.p'
VALUESPATH = os.path.join(PICKLE_DIR, VALUES)

with open(VALUESPATH, 'rb') as f:
    values = pickle.load(f)

class main ():
    def __init__(self):
        self.productCost = 0
        self.factoryLevel = 1
        self.amountProduced = 2^self.factoryLevel*2
        self.income = self.productCost * self.amountProduced
        self.upgrade = self.income * 5
        self.materialCost = 0 #Changed in other classes
        self.profit = self.income - (self.materialCost * self.amountProduced)

class steel (main):
    def __init__(self):
        super().__init__()
        self.materialCost = values.steelMineValue

#Profit = (Income) - (Material Cost * Amount Produced) - (Amount of workers * Worker Salary) {If less than $0, profit is $0}
#Material Cost = Each resource * Resource cost