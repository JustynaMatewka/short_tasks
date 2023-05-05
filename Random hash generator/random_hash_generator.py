import hashlib
import random
import time


def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

def sha_256(text):
    m = hashlib.sha256()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

def sha_3(text):
    m = hashlib.sha3_256()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

def sha_1(text):
    m = hashlib.sha1()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

def blake2s(text):
    m = hashlib.blake2s()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

def random_string(length):  # Losowe łańcuchów znaków
    return ''.join(chr(random.randint(32, 126)) for x in range(length))



ranges = int(input())
random_str = [[x, []] for x in [5, 10, 20, 50, 100, 200]]
hashed_strs = [[x, []] for x in [5, 10, 20, 50, 100, 200]]

for i in range(ranges):
    length = random.choice([5, 10, 20, 50, 100, 200])
    for x in random_str:
        if length == x[0]: x[1].append(random_string(length))



functions = [md5, sha_256, sha_3, sha_1, blake2s]

for length in range(len(random_str)):
    print(f"String length: {random_str[length][0]}")

    for f in functions:
        collisions = 0
        start_time = time.time()

        for word in random_str[length][1]:
            hashed_strs[length].append(f(word))
            if hashed_strs[length].count(hashed_strs[length][-1]) > 1: collisions += 1

        end_time = time.time()

        print(f"{f.__name__}: time {(end_time - start_time):.4f} seconds, collisions: {collisions}")
    print()