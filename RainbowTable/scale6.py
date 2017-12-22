import conversions
import hashlib
import random
import pickle
import string


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


def reduce_git1(hashb64, column):
    hashhex = conversions.b64_to_hex(hashb64)
    hashV = hashhex
    z = b26_to_num('z')
    results = []
    chars = 'abcdefghijklmnopqrstuvwxyz'
    # Cast hash from str to int then decompose into bytes
    byteArray = getBytes(hashV)
    for i in range(6):
        index = byteArray[(i + column) % len(byteArray)]
        newChar = chars[index % len(chars)]
        results.append(newChar)
    "".join(results)
    results[3] = num_to_b26((b26_to_num(results[3]) + column) % z, 1)
    pword = "".join(results)
    return pword


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
    random_string = num_to_b26(random.randint(0, b26_to_num('zzzzzz')), 6)
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


def maketb6_full():
    rainbow = {}
    r10ps = []
    allsps = []
    alleps = []
    rows = 0
    while rows < 90000:   # 6500 in scale4full
        if rows % 10 == 1:
            print rows-1
        sp = generate_pword()
        temp = sp
        ep = ''
        for cols in range(0, 3400, 1):   # 70 in scale4full
            ep = hashfunc(temp)
            temp = reduce_git1(ep, cols)
        rainbow[ep] = sp
        allsps.append(sp)
        alleps.append(ep)
        rows += 1
    return rainbow, allsps, alleps


def choose_chain41(tbl, h):
    print '--------BEGIN CHOOSE----------'
    originalhash = h
    lastreduction = -1
    cols = 3398
    if h in tbl:
        chain = tbl[h]
        return chain, h, lastreduction
    else:
        for i in range(cols, -1, -1):
            if h in tbl:
                print 'break1'
                print tbl[h], h
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
        chain = tbl[h]
        return chain, h, lastreduction


def hashreduceloop(start, h):
    for i in range(start, 3399, 1):
        # print i
        h = hashfunc(reduce_git1(h, i))
    return h


def traverse_chain4(chain, h, start):
    print ' ---------BEGIN TRAVERSE----------'
    # print'Beginning of chain: ' + chain
    chainbegin = chain
    currentcolnum = 0
    # testarr = []
    cols = 3400
    counter = start
    for i in range(counter, cols, 1):
        # testarr.append(chain)
        if hashfunc(chain) == h:
            break
        else:
            chain = hashfunc(chain)
            print i, counter      # NEED TO LOOK CLOSER AT THIS LOOP, PROB WRONG
            chain = reduce_git1(chain, i)  # LIKE HAD TO USE HASHLOOPREDUCE()
            counter += 1
    if hashfunc(chain) == h:
        # print hashfunc(chain), h
        return chain, True
    else:
        print 'used all reductions in traverse '
        print counter
        if counter > 3400:
            return traverse_chain4(chain, h, counter)
        return chain, False


def crack4full(rb, hsh):
    print '[------begin crack4full----------]'
    chain, chainep, lastreduction = choose_chain41(rb, hsh)
    print hsh
    if chain == 0:
        print 'couldnt locate a chain'
        return
    pword, tf = traverse_chain4(chain, hsh, 0)
    if hashfunc(pword) != hsh:
        newrb = rb
        del newrb[chainep]
        print 'row deleted'
        crack4full(newrb, hsh)
    else:
        return pword
