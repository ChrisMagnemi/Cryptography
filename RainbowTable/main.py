import hashlib
import pickle
import random
import conversions


hashes =['7iEjysAibZbmoZP/9v5w3MPnUW0=', 'RKlxM1DlOFjwWEY9S/fx5ULZyks=',
'xoq93JEjOAYSE8V/a0EZx5Ggefg=',
'ZHfX8f2/uYMwyRSnf08iCrqE8Es=',
'Qf4I/A3UTnn3mdA+zpA+Yr4l3H0=',
'qwaEUA9V60H/7EDP4cKZY/x36NI=',
'5en6G6MezRroT3XKqkdPOmY/BfQ=',
'MCdMR5A70brHYzu/CXQxSeurgF8=',
'TcxBc9gKKBcgbhlqOPDb94UBiP8=',
'UhmdfQG4AZO9sAhg4J4leQaIVog=',
'5yfRRkrhJDbomacm2lsvEdg4GyY=',
'+Amz21UcTXh4gTZfcEWvdFpElHw=',
'cP/Cgdvsjaz04C6HnG4gqTsazVk=',
'U7ChsvrfTgQM3CFVpzQN4krKk8s=',
'YcmysX23eieEG77qv/kjRIsPY4g=',
'HdCbqhncdoj5bi6kUDNgOSHNe4M=',
'URbkBpSsSPZUy3toFhd+DnFyN8Y=',
'8JdPAcmCX8LO9tdtJo5vmTzlPCA=',
'7/oeoFeAObRnjfB+GXdqQEF6jD0=', 'q2XYuWEftY9MYS9qXsI54Oc/04w=']


# returns hash of input as b64
def hashfunc(s):
    hashedvalue = hashlib.sha1(s).hexdigest()
    hashasb64 = conversions.hex_to_b64(hashedvalue)
    return hashasb64


def most_common(lst):
    return max(set(lst), key=lst.count)


def save_obj(obj, name):
    pathname = '/Users/ChrisMagnemi/Desktop/BC_Spring_2016/Crpytography/RainbowTables/'
    with open(pathname + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    pathname = '/Users/ChrisMagnemi/Desktop/BC_Spring_2016/Crpytography/RainbowTables/'
    with open(pathname + name + '.pkl', 'rb') as f:
        return pickle.load(f)


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
    random_string = num_to_b26(random.randint(0, 26**6), 6)
    return random_string


def hashreduceloop(index, h, chainlength):
    for i in range(index, chainlength-1, 1):
        r = rdc(h, i)
        h = hashfunc(r)
    return h


def rdc(hsh, index):
    hsh_num = b64_to_bits(hsh)
    reduction = (hsh_num + index) % (26**6)
    return num_to_b26(reduction, 6)


def makerb6(numchains, chainlength):
    rb = {}
    r5ps = []
    chain_i = 1
    while chain_i <= numchains:
        if chain_i % 100 == 1:
            print chain_i - 1
        sp = generate_pword()
        temp = sp
        ep = ''
        j = 0
        while j < chainlength:
            if chain_i == 5:
                r5ps.append(temp)
            ep = hashfunc(temp)
            temp = rdc(ep, j)
            j += 1
        rb[ep] = sp
        chain_i += 1
    return rb, r5ps


def choosechain(rb, goalhash, index, chainlength):
    # print '------Begin chainChoose-------'
    h = goalhash
    if h in rb:
        return rb[h], -1
    else:
        while h not in rb:
            h = hashreduceloop(index, goalhash, chainlength)
            index += 1
            if index > chainlength:
                h = 'could not locate a chain'
                return h, chainlength + 10
    return rb[h], index


def traversechain(chain, goalhash, index, chainlength):
    isFound = 0
    while hashfunc(chain) != goalhash:
        chainhsh = hashfunc(chain)
        chain = rdc(chainhsh, index)
        index += 1
        if index > chainlength:
            isFound = -1
            break
    if isFound > -1:
        return chain, index
    else:
        # print 'print: checked whole chain'
        return 'checked whole chain', -10


def crack6(rb, goalhash, chainlength):
    chooseindex = 0
    password = 'not found yet'
    while password == 'not found yet' or password == 'checked whole chain':
        traverseindex = 0
        chain, chooseindex = choosechain(rb, goalhash, chooseindex, chainlength)
        # print chain, chooseindex
        # chooseindex += 1
        password, traverseindex = traversechain(chain, goalhash, traverseindex, chainlength)
        if chooseindex+1 > chainlength:
            return 'could not crack password'
    return password


def crackall(rb, chainlength):
    for i in range(0, len(hashes)):
        print i, crack6(rb, hashes[i], chainlength)














