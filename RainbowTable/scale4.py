import conversions
import hashlib
import random
import pickle


def generate_pword():
    lowcase_letters = 'abcdefghijklmnopqrstuvwxyz'
    random_string = ''
    i = 0
    while i < 4:
        x = random.randint(0, 25)
        random_string += lowcase_letters[x]
        i += 1
    return random_string

def save_obj(obj, name):
    pathname = '/Users/ChrisMagnemi/Desktop/BC_Spring_2016/Crpytography/RainbowTables/'
    with open(pathname + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    pathname = '/Users/ChrisMagnemi/Desktop/BC_Spring_2016/Crpytography/RainbowTables/'
    with open(pathname + name + '.pkl', 'rb') as f:
        return pickle.load(f)

h =['7iEjysAibZbmoZP/9v5w3MPnUW0=', 'RKlxM1DlOFjwWEY9S/fx5ULZyks=',
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


def reduce_git(hashb64, column):
    hashhex = conversions.b64_to_hex(hashb64)
    hashV = hashhex[:10]
    results = []
    chars = 'abcdefghijklmnopqrstuvwxyz'
    # Cast hash from str to int then decompose into bytes
    byteArray = getBytes(hashV)
    for i in range(4):
        index = byteArray[(i + column) % len(byteArray)]
        newChar = chars[index % len(chars)]
        results.append(newChar)
    return "".join(results)


def r1(hashval, colindex):
    pwordspace = b26_to_num('zzzz')
    hash_as_bits = b64_to_bits(hashval)
    # result = (hash_as_bits + 65536*rowindex + colindex) % pwordspace
    result = (hash_as_bits + 65536 * colindex) % pwordspace
    result_as_str = num_to_b26(result)
    return result_as_str


def r2(hashval, colindex):
    param3 = colindex
    passwordspace = b26_to_num('zzzz')
    hash_as_bits = b64_to_bits(hashval[:8])
    result = (hash_as_bits * param3 + colindex) % passwordspace
    # result = (kthroot(hash_as_bits, colindex) + colindex * param3)**2 % passwordspace
    arg1 = result % passwordspace
    arg2 = (hash_as_bits-colindex) % passwordspace
    # print arg1, arg2
    result2 = conversions.xor(num_to_b26(arg1, 4), num_to_b26(arg2, 4))
    result3 = b64_to_bits(conversions.as_to_b64(result2)) % passwordspace
    return num_to_b26(result3, 4)


def r3(hashval, col):
    passwordspace = b26_to_num('zzzz')
    hashsmall = (b64_to_bits(hashval[:8]))
    result = conversions.xor(num_to_b26(hashsmall, 4), num_to_b26(col, 4))
    result = conversions.as_to_b64(result)
    result = b64_to_bits(result) % passwordspace
    return num_to_b26(result, 4)


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


# def tbl_size4():
#     rainbow = {}
#     rows = 0
#     while rows < 250:
#         sp = generate_pword()
#         temp = sp
#         ep = ''
#         for cols in range(0, 1999, 1):
#             ep = hashfunc(temp)
#             temp = r2(ep, cols)
#         rainbow[ep] = sp
#         print rows
#         rows += 1
#     return rainbow


def maketb4_2():
    rainbow = {}
    tbltestep = []
    tbltestsp = []
    r46ps = []
    tbpasswords = []
    rows = 0
    while rows < 100:
        # print rows
        sp = generate_pword()
        temp = sp
        ep = ''
        for cols in range(0, 20, 1):
            ep = hashfunc(temp)
            print cols
            r46ps.append(temp)
            temp = reduce_git(ep, cols)
        rainbow[ep] = sp
        tbltestep.append(ep)
        tbltestsp.append(sp)
        # print rows
        rows += 1
    return rainbow, r46ps


def count_distinct(arr):
    distinct = []
    for i in range(0, len(arr)):
        if arr[i] not in distinct:
            distinct.append(arr[i])
    return distinct


def most_common(lst):
    return max(set(lst), key=lst.count)


def choose_chain4(tbl, h):
    print '--------BEGIN CHOOSE----------'
    cols = 20
    rows = 250
    for i in range(0, cols, 1):
        # print i
        if h in tbl:
            break
        else:
            h = reduce_git(h, i)
            h = hashfunc(h)
    if h in tbl:
        ep = h
        chain = tbl[h]
        return chain, ep
    else:
        return choose_chain4(tbl, h)


def traverse_chain4(chain, h, start):
    print ' ---------BEGIN TRAVERSE----------'
    print'Beginning of chain: ' + chain
    chainbegin = chain
    testarr = []
    cols = 449
    counter = start
    for i in range(start, cols, 1):
        testarr.append(chain)
        if hashfunc(chain) == h:
            print 'found it!'
            break
        else:
            chain = hashfunc(chain)
            if i == 0:
                print i
            chain = reduce_git(chain, i)
            counter += 1
    if hashfunc(chain) == h:
        print hashfunc(chain), h
        return chain, True
    else:
        print 'else of traverse with chain: ' + chain
        counter += 1
        return chainbegin, chain, False


def crack4(rb, h, i):
    chain, ep = choose_chain4(rb, h)
    p, isCorrect = traverse_chain4(chain, h, i)
    if isCorrect == False:
        if ep in rb:
            del rb[ep]
            crack4(rb, h, 0)
        else:
            return 'WRONG!'
    else:
        print "should be correct!!"
        return p
