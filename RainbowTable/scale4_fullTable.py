import conversions
import hashlib
import random
import pickle
import string
from itertools import groupby


def hashfunc(s):
    hashedvalue = hashlib.sha1(s).hexdigest()
    hashasb64 = conversions.hex_to_b64(hashedvalue)
    return hashasb64


def getBytes(hashV):
    results = []
    remaining = int(hashV, 16)
    while remaining > 0:
        results.append(remaining % 256)
        remaining //= 256
    return results


# def reduce_git(hashb64, column):
#     hashhex = conversions.b64_to_hex(hashb64)
#     hashV = hashhex[:10]
#     results = []
#     chars = 'abcdefghijklmnopqrstuvwxyz'
#     # Cast hash from str to int then decompose into bytes
#     byteArray = getBytes(hashV)
#     for i in range(4):
#         index = byteArray[(i + column) % len(byteArray)]
#         newChar = chars[index % len(chars)]
#         results.append(newChar)
#     return "".join(results)

def reduce_git1(hashb64, column):
    hashhex = conversions.b64_to_hex(hashb64)
    hashV = hashhex
    results = []
    chars = 'abcdefghijklmnopqrstuvwxyz'
    # Cast hash from str to int then decompose into bytes
    byteArray = getBytes(hashV)
    for i in range(4):
        index = byteArray[(i + column) % len(byteArray)]
        newChar = chars[index % len(chars)]
        results.append(newChar)
    letter4 = results[3]
    letter4num = ((b26_to_num(letter4)) + column) % 26
    newletter4 = num_to_b26(letter4num, 1)
    # if column > 100:
    #     pword = "".join(results)
    return "".join(results)


# converts a number between 0 and 26^6 - 1 to lowercase alphas
# returns string between 'aaaaaa' and 'zzzzzz'
def num_to_b26(num, length):
    b26string = ''
    for i in range(length-1, -1, -1):
        j = i
        if (num / 26**j) > 0:
            exp = num / 26**j
            b26string += chr(exp + ord('a'))
            num -= 26**j * exp
        else:
            b26string += 'a'
    return b26string


# converts a base 26 password to a number wahoo!!!
def b26_to_num(b26rep):
    alphas = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm':12, 'n': 13, 'o':14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}
    num = 0
    length = len(b26rep)
    for i in range(length-1, -1, -1):
        const = alphas[b26rep[i]]
        num += const * 26**(length-i-1)
    return num


def b64_to_bits(b64text):
    text = conversions.b64_to_hex(b64text)
    bits = int(text, 16)
    return bits


def generate_pword():
    random_string = num_to_b26(random.randint(0, b26_to_num('zzzz')), 4)
    return random_string


def save_obj(obj, name):
    pathname = '/Users/ChrisMagnemi/Desktop/BC_Spring_2016/Crpytography/RainbowTables/'
    with open(pathname + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    pathname = '/Users/ChrisMagnemi/Desktop/BC_Spring_2016/Crpytography/RainbowTables/'
    with open(pathname + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def most_common(lst):
    return max(set(lst), key=lst.count)


def maketb4_full():
    rainbow = {}
    r10ps = []
    r10hs = []
    r11ps = []
    r12ps = []
    r13ps = []
    allsps = []
    alleps = []
    rows = 0
    while rows < 6500:
        if rows % 100 == 1:
            print rows-1
        sp = generate_pword()
        temp = sp
        ep = ''
        for cols in range(0, 70, 1):
            ep = hashfunc(temp)
            if rows == 11:
                r11ps.append(temp)
            if rows == 12:
                r12ps.append(temp)
            if rows == 10:
                r10ps.append(temp)
                r10hs.append(ep)
            if rows == 13:
                r13ps.append(temp)
            temp = reduce_git1(ep, cols)
        rainbow[ep] = sp
        allsps.append(sp)
        alleps.append(ep)
        rows += 1
    return rainbow, r13ps, r11ps, allsps, alleps


def choose_chain41(tbl, h, start):
    print '--------BEGIN CHOOSE----------', start
    originalhash = h
    lastreduction = -2
    if h in tbl:
        print 'break1'
        chain = tbl[h]
        return chain, h, lastreduction
    else:
        for i in range(start, -1, -1):
            print i
            if h in tbl:
                print 'break2'
                break
            else:
                h = originalhash
                h = hashreduceloop(i, h)
                lastreduction = i
                #   h = hashfunc(h)
    if h not in tbl:
        # return choose_chain41(tbl, h)
        return 0, 0, lastreduction
    else:
        print 'choose last else'
        chain = tbl[h]
        return chain, h, lastreduction


def hashreduceloop(start, h):
    for i in range(start, 69, 1):
        r = reduce_git1(h, i)
        # return r, i
        h = hashfunc(r)
    return h


def traverse_chain4(chain, h, start):
    print ' ---------BEGIN TRAVERSE----------', chain, h
    cols = 70
    counter = start
    print 'start is:, ', start
    for i in range(start, cols, 1):
        if hashfunc(chain) == h:
            return chain, True
        else:
            chain = hashfunc(chain)
            chain = reduce_git1(chain, i)
            counter += 1
    print chain, h, counter
    if hashfunc(chain) == h:
        # print hashfunc(chain), h
        return chain, True
    else:
        print 'used all reductions in traverse '
        if counter < 70:
            print 'counter less than 70'
            return traverse_chain4(chain, h, counter)
        return chain, False


def crack4(rb, goalhash, start):
    print '[[[[[[[[[[[[[ crack4 ]]]]]]]]]]'
    currenthash = goalhash
    lastreduction = start
    while 1:
        print 'crack while loop, start is ', 69 - start
        chain, chainep, lastreduction = choose_chain41(rb, currenthash, 69 - start)
        print 'chose:', chain, chainep
        nextreduction = lastreduction + 1
        print 'next reduction'
        print nextreduction
        if chain == 0:  # means chain endpoint is not in rb anywhere
            print 'could not locate a chain'
            return
        else:           # found a chain, so traverse it looking for original hash
            pword, tf = traverse_chain4(chain, goalhash, 0)
        if tf == True:  # found the correct password
            return pword
        elif start == -1:   # too many reductions done, can't find a chain
            return 'could not crack password'
        else:           # FALSE ALARM, chose wrong chain, now continue looking for another chain
            print 'FALSE ALARM',  nextreduction
            currenthash = hashreduceloop(nextreduction - 1, chainep)
            start = 69 - nextreduction + 1
            print currenthash, chainep, lastreduction
