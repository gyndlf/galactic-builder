# Load all users into an array called "users"
import pickle
import os, sys

MY_DIR  = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')

users = []

with open(fname, 'rb') as f:
    person = pickle.load(f)