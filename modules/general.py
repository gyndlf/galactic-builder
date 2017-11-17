# The general functions needed to run the code
import logging
import random
import string as s

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def randomchars(seed):
    """Returns two randomised dictionaries"""
    random.seed(seed)

    chars = s.printable[:-5]  # All valid characters
    logger.debug('All characters %s', chars)
    chars = chars.replace("\\", "")  # Remove backslash
    chars = chars.replace("'", '')  # Remove single quote
    chars = chars.replace('"', '')  # Remove double quote
    chars = chars.replace(',', '')  # Remove commar
    chars = chars.replace('`', '')  # Remove thingy
    word = list(chars)
    logger.debug('Valid character %s', chars)
    random.shuffle(word)
    chars = ''.join(word)
    logger.debug('Shuffled characters %s', chars)
    substution = chars[-3:] + chars[:-3]  # Moves them over by 3

    # Create the encryption and decryption dictionaries
    encryption = {}
    decryption = {}
    for i, c in enumerate(chars):
        v = substution[i]
        encryption[c] = v
        decryption[v] = c

    return encryption, decryption


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


if __name__ == '__main__':  # The file is run directly
    print('Error 321: Unknown values')
