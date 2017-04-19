# This is THE file to use when wanting to edit the database
# This used to be 7 seperate files but they have been merged into one

import pickle
import os, sys

# Calculate file paths
MY_DIR = os.path.realpath(os.path.dirname(__file__))
PICKLE_DIR = os.path.join(MY_DIR, 'data')
USERS = "users.p"
USERSPATH = os.path.join(PICKLE_DIR, USERS)
DATABASE = 'database.p'
DATABASEPATH = os.path.join(PICKLE_DIR, DATABASE)
VALUES = 'values.p'
VALUESPATH = os.path.join(PICKLE_DIR, VALUES)


def editUser():
    # Edits a specified user. Has failsafe built in
    # Create file name
    name = str(input("Username? "))
    filename = name + ".p"

    # Finish making file path
    fname = os.path.join(PICKLE_DIR, filename)
    print("Opening " + str(fname))

    # Open and save the varible from the file
    try:
        with open(fname, 'rb') as f:
            person = pickle.load(f)
    except:
        print("Error: User does not exist")
        return

    print("Loaded user " + person.name)
    print("Current varibles: " + str(vars(person)))
    edit = str(input("Varible to edit? "))

    try:
        value = getattr(person, edit)
    except:
        print("Error: No varible name")
        return
    print("Current value is " + str(value))

    kind = input("Is this new value a string or int (s or i)? ")
    if kind == "s" or kind == "S":
        new = str(input("What should the new value be? "))
    elif kind == "i" or kind == "I":
        new = int(input("What should the new value be? "))
    else:
        print("Invaild option.")
        return

    setattr(person, edit, new)
    check = getattr(person, edit)
    print("Updated the value to " + str(check))

    with open(fname, 'wb') as f:
        pickle.dump(person, f)
    print("Done.")


def createUser():
    # Creates a new user with no money, jobs or anything according to the "database.py" file and add them into a list stored in "users.p"
    print("Warning! Names CANNOT be changed! Think carefully...")
    import database

    name = input("User name? ")
    # user = input("User id? ")
    password = input("User password? ")

    # Create the user in RAM
    created = database.person()
    created.name = name
    created.password = password

    # Work out file names
    filename = str(created.name) + ".p"
    fname = os.path.join(PICKLE_DIR, filename)
    print("Creating " + str(fname))

    # Add users to the list of users
    with open(USERSPATH, 'rb') as f:
        users = pickle.load(f)
    print("Adding " + name + " to " + USERS)
    users.append(filename)
    print("Current users " + str(users))
    with open(USERSPATH, 'wb') as f:
        pickle.dump(users, f)

    # Save the finished product
    with open(fname, 'wb') as f:
        pickle.dump(created, f)
    print("Created")
    print("Done")


def removeUser():
    # Removes a user from 'users.p' so you can delete their file
    print('These changes are irreversible! Are you sure you want to continue? (y/n)')
    choice = input(": ")
    go = False
    if choice == "y":
        go = True
    if go == False:
        return

    # Find filenames
    name = input("Username? ")
    filename = name + ".p"
    with open(USERSPATH, 'rb') as f:
        users = pickle.load(f)

    # Remove user
    print("Removing " + name + " from " + USERS)
    try:
        users.remove(filename)
    except:
        print("Error: No such user")
        return

    # Save new data
    print("Current users " + str(users))
    with open(USERSPATH, 'wb') as f:
        pickle.dump(users, f)

    print("You may now delete " + filename + ' safely.')


def loadUsers():
    # Load all users according to "users.p" and display their stats

    with open(USERSPATH, 'rb') as f:
        users = pickle.load(f)
    print('Current users ' + str(users))

    for file in users:
        fname = os.path.join(PICKLE_DIR, file)
        print('')
        print("Opening " + str(fname))
        with open(fname, 'rb') as f:
            person = pickle.load(f)
        print(vars(person))


def updateVaribles():
    # This code will add a new varible(s) to all of the users in the data file.
    # This is done according to database.py
    import database
    import baseValues

    confirm = False
    print(
        'You are about to update the entire database. If this goes wrong EVERYTHING WILL BE LOST. Triple check before contuning')
    print('You cannot remove varibles (yet) only add so everything is PERMENENT!')
    print('Edit "database.py" to update the varibles. Be CAREFUL!')
    if str(input('Are you sure you want to continue? ')) == 'y':
        confirm = True
    if confirm == False:
        return

    # Load all the users currently made
    with open(USERSPATH, 'rb') as f:
        users = pickle.load(f)

    # Load database.p
    with open(DATABASEPATH, 'rb') as f:
        oldData = pickle.load(f)
    oldVars = vars(oldData)

    # Load new database
    newData = database.person()
    newVars = vars(newData)

    # Find the changes
    change = []
    for varible in newVars:
        try:
            oldVars[varible]
        except:
            change.append(varible)
    print('')
    print('Found  ' + str(change) + ' new changes')

    # For person in users change their varible(s)
    for file in users:
        fname = os.path.join(PICKLE_DIR, file)
        print("Opening " + str(fname))

        # Open the file
        with open(fname, 'rb') as f:
            person = pickle.load(f)

        # Find person current varibles
        current = vars(person)
        print("Old : " + str(current))

        # Add changes
        for diff in change:
            print("Need to add " + diff)
            current[diff] = newVars[diff]

        print("New : " + str(current))

        with open(fname, 'wb') as f:
            pickle.dump(person, f)
        print('')

    # Save the new database.py to the database.p file
    print('Saving new database...')
    with open(DATABASEPATH, 'wb') as f:
        pickle.dump(newData, f)

    # Do the same with the values:
    print("Moving on to values.p")

    # Work out names
    VALUES = 'values.p'
    VALUESPATH = os.path.join(PICKLE_DIR, VALUES)

    # Load values.p
    with open(VALUESPATH, 'rb') as f:
        oldValues = pickle.load(f)
    oldVarsv = vars(oldValues)

    # Load new values
    newValues = baseValues.basic()
    newVarsv = vars(newValues)

    # Find the changes
    changes = []
    for varible in newVarsv:
        try:
            oldVarsv[varible]
        except:
            changes.append(varible)

    print("Found " + str(changes) + ' changes.')
    print('Old : ' + str(oldVarsv))

    # Add changes
    for diff in changes:
        print("Need to add " + diff)
        oldVarsv[diff] = newVarsv[diff]

    print("New : " + str(oldVarsv))

    with open(VALUESPATH, 'wb') as f:
        pickle.dump(newValues, f)

    print('Done.')


def createDatabase():
    # This code will initilise the database You probably will run it when you start from scratch
    import database
    import baseValues

    confirm = False
    print('This will create "database.p", "users.p" and "values.p"')
    print('Only run this when there is no files in the data folder. It will create the scaffolding for them')
    if str(input('Are you sure you want to continue? ')) == 'y':
        confirm = True
    if confirm == False:
        return

    users = []
    with open(USERSPATH, 'wb') as f:
        pickle.dump(users, f)

    # Load data
    data = database.person()
    values = baseValues.basic()

    # Save it!
    with open(DATABASEPATH, 'wb') as f:
        pickle.dump(data, f)
    with open(VALUESPATH, 'wb') as f:
        pickle.dump(values, f)

def payUsers():
    #Load users
    #For user in users
    #Add money by income
    #save

    with open(USERSPATH, 'rb') as f:
        users = pickle.load(f)

    for file in users:
        fname = os.path.join(PICKLE_DIR, file)
        print('')
        print("Opening " + str(fname))
        with open(fname, 'rb') as f:
            person = pickle.load(f)
        print(person.name, ' now has ', person.netIncome, ' more money with a total of ', person.money + person.netIncome)
        person.money += person.netIncome

        with open(fname, 'wb') as f:
            pickle.dump(person, f)


def main():
    quit = False
    while quit == False:
        # Main page
        print("-" * 10 + "Home" + "-" * 10)
        print("Welcome to the usermanagement system! Here you can do anything you want to the database.")
        print("Press 1 to create a user")
        print("Press 2 to edit a user")
        print("Press 3 to remove a user")
        print("Press 4 to view all users")
        print("Press 5 to update varibles in the database.py and values.p")
        print("Press 6 to create a new database")
        print("Press 7 to give the users their income")
        print("Or press anything else to quit")

        choice = input(": ")

        if choice == "1":
            # Create a users
            # Uses createUser.py
            print("-" * 10 + "Creating User" + "-" * 10)
            createUser()

        elif choice == "2":
            # Edit a user
            # Uses edituser.py + loadUser.py
            print("-" * 10 + "Editing User" + "-" * 10)
            editUser()

        elif choice == "3":
            # Remove a user
            # Uses removeUser.py
            print("-" * 10 + "Removing User" + "-" * 10)
            removeUser()

        elif choice == "4":
            # View all users
            # Uses LoadAllUsers.py
            print("-" * 10 + "Loading Users" + "-" * 10)
            loadUsers()

        elif choice == "5":
            # Update varibles
            # Uses updateVaribles.py and LoadAllUsers.py and editUsers.py
            print("-" * 10 + "Updating Varibles" + "-" * 10)
            updateVaribles()

        elif choice == "6":
            # Create new database
            # Uses createDatabase.py
            print("-" * 10 + "Creating Database" + "-" * 10)
            createDatabase()

        elif choice == '7':
            #Adds the users salary
            #Newly created code
            print('-'*10 + 'Paying Users' + '-'*10)
            payUsers()

        else:
            print("Quitting...")
            quit = True


if __name__ == '__main__':
    main()
