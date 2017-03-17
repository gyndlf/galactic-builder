# Load the specified user
import pickle
import os, sys

MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

name = str(input("Username? "))
filename = name + ".p"

fname = os.path.join(PICKLE_DIR, filename)
print("Opening " + str(fname))

with open(fname, 'rb') as f:
    person = pickle.load(f)

print(vars(person))