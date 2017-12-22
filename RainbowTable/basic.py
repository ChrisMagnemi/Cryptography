import hashlib
import random
import string
import conversions
import pickle


# returns hash of input as b64
def hashfunc(s):
    hashedvalue = hashlib.sha1(s).hexdigest()
    hashasb64 = conversions.hex_to_b64(hashedvalue)
    return hashasb64


# takes b64 hash and some parameters to return a string password
# a password has to be 6 lowercase letters
# param2 cannot be greater than 15
def reduce(hashval, reductionType, param2):
    if reductionType == 1:
        hashLetters = onlyLetters(hashval)
        reduceval = hashLetters[param2:param2+6]
    elif reductionType == 2:
        hashLetters = onlyLetters(hashval)
        nextval = hashLetters[param2:param2+6]
        reduceval = nextval[::-1]
    else:
        # print('shiiittt')
        reduceval = 'aaaaaa'
    return reduceval.lower()


# returns the letters only from a b64 value
def onlyLetters(b64hash):
    posLetters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    response = ''
    for char in b64hash:
        if char in posLetters:
            response += char
    return response


# generates a random 'password' of 6 lowercase letters
def generate_pword():
    lowcase_letters = 'abcdefghijklmnopqrstuvwxyz'
    random_string = ''
    i = 0
    while i < 6:
        x = random.randint(0, 25)
        random_string += lowcase_letters[x]
        i += 1
    return random_string


# function to actually create a rainbow table
def createRainbow():
    tablename = {}
    num_start_pts = 0
    reductiontype = 1
    while num_start_pts < 200:
        if num_start_pts == 100:
            reductiontype += 1
        if reductiontype == 1:
            param2 = 0
            sp = generate_pword()
            initializer = hashfunc(sp)
            while param2 < 16:
                r1 = reduce(initializer, reductiontype, param2)
                initializer = hashfunc(r1)
                param2 += 1
            ep = initializer
            tablename[ep] = sp
            num_start_pts += 1
        if reductiontype == 2:
            param2 = 0
            sp = generate_pword()
            initializer = hashfunc(sp)
            while param2 < 16:
                r1 = reduce(initializer, reductiontype, param2)
                initializer = hashfunc(r1)
                param2 += 1
            ep = initializer
            tablename[ep] = sp
            num_start_pts += 1
    return tablename
    # now save tablename somehow for future use


# saves a dictionary externally
def save_obj(obj, name):
    pathname = '/Users/ChrisMagnemi/Desktop/BC_Spring_2016/Crpytography/RainbowTables/'
    with open(pathname + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    pathname = '/Users/ChrisMagnemi/Desktop/BC_Spring_2016/Crpytography/RainbowTables/'
    with open(pathname + name + '.pkl', 'rb') as f:
        return pickle.load(f)


# determines which chain to follow, in other words
# goes through the rainbow dictionary and determines the proper starting point
def choose_row(rainbow, hash_to_crack):
    if hash_to_crack in rainbow:
        return rainbow[hash_to_crack]
    else:
        param2 = 15
        reduc_type = 2
        while hash_to_crack not in rainbow:
            r1 = reduce(hash_to_crack, reduc_type, param2)
            hash_to_crack = hashfunc(r1)
            print(r1, hash_to_crack)
            param2 -= 1
            if param2 < 0:
                reduc_type -= 1
        return rainbow[hash_to_crack]


# traverse a chain to find the hash that matches the original
# input, then return the preceding password as the cracked password
def traverse_row(startpt, oghash):
    reduc_type = 1
    param2 = 0
    hash1 = hashfunc(startpt)
    if hash1 == oghash:
        return startpt
    else:
        r1 = reduce(hash1, reduc_type, param2)
        traverse_row(r1, oghash)
