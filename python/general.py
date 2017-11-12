# The general functions needed to run the code
import logging
import pickle
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def loadusers(userfilepath, pickledir):
    """Load users from the file given as USERS"""
    logger.info('[1] Loading users')
    users = []
    # Load users.p files
    with open(userfilepath, 'rb') as f:
        usersarray = pickle.load(f)

    # Read to find out the users
    for file in usersarray:
        fname = os.path.join(pickledir, file)
        with open(fname, 'rb') as f:
            person = pickle.load(f)
            users.append(person)
    return users


def loadvalues(valuefilepath):
    """Load the values from the file given as VALUES"""
    logger.info('[1] Load values')
    with open(valuefilepath, 'rb') as f:
        values = pickle.load(f)
    return values


def scramblecookie(request, username, encryptdict):
    """Scramble the username and add to the give request"""
    t = []
    for i in username:
        v = encryptdict[i]
        t.append(v)
    sessio = ''.join(t)
    request.set_cookie('sessionID', sessio)
    return request


def loadcookie(username, decryptdict):
    """Decrypt the username"""
    # Converts the cypher to words.
    h = []
    for i in username:
        v = decryptdict[i]
        h.append(v)
    return ''.join(h)


def hasmoney(person, money):
    """Weather or not the object has >= money"""
    try:
        if person.money >= money:
            return True
        else:
            return False
    except:  # Don't know how to make exception clauses specific yet. Well. I do just haven't tried
        return False


if __name__ == '__main__':
    print('Running general.py directly')
