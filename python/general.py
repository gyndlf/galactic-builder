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


if __name__ == '__main__':
    print('Running general.py directly')
