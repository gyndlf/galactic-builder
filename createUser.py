import pickle

# Creates a new user with no money, jobs or anything according to the database.py file

import database

name = input("User name? ")
user = input("User id? ")

created = database.person

created.name = name
created.id = user


