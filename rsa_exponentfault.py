#!/usr/bin/env python

import random
from collections import Counter
from Crypto.PublicKey import RSA

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b / a) * y, y)

def modinv(a, n):
    g, x, y = egcd(a, n)
    if g != 1:
        return None
    else:
        return x % n

# TODO add comments
# TODO add printed comments

print "In this sample we show how to recover the secret exponent d, when standard unpadded RSA (non-CRT) is used to sign, but random bitflips affects d"

m = 123456789 # m has to be known
key = RSA.generate(1024)
# key.d is secret
# key.n and key.e are public

cc = 0

def rsa_sign(c,d,n):
    return pow(c,d,n)

def rsa_enc(m,e,n):
    return pow(m,e,n)

def rsa_sign_broken(c,d,n):
    rnd = random.randint(0,1)
    if rnd == 0:
        # randomly flip one bit
        rnd = random.randint(0,1023)
        d = d ^ (1 << rnd)
    return rsa_sign(c,d,n)

print "Getting a lot of signatures of the message %d..." % m
alot_of_signatures = [rsa_sign_broken(m,key.d,key.n) for _ in xrange(25000)]

#import pickle; alot_of_signatures = pickle.load(open("pp"))
'''
import pickle
pickle.dump(alot_of_signatures,open("pp","wb"))
alot_of_signatures = pickle.load(open("pp"))
'''

N = key.n

# find the good signature
cc = Counter(alot_of_signatures)
good_sig = max(cc.iteritems(),key=lambda x:x[1])[0]

print "Computing flips..."
# TODO add mathematical explanation
flipbit_plus = [(good_sig * pow(m, 1 << bit, N)) % N for bit in xrange(1024)]
flipbit_minus = [(good_sig * modinv(pow(m, 1 << bit, N), N)) % N for bit in xrange(1024)]

print "Finding flips..."
bits_of_d = {}
for sig in alot_of_signatures:
    if sig == good_sig:
        continue
    for bit in xrange(1024):
        if sig == flipbit_plus[bit]:
            bits_of_d[bit] = 0
            # print "1->0",bit
            break
        elif sig == flipbit_minus[bit]:
            bits_of_d[bit] = 1
            # print "0->1",bit
            break
    else:
        print "flip not found"

recovered_d = 0
for k,v in bits_of_d.iteritems():
    recovered_d += v << k

print "d is:", recovered_d
assert key.d == recovered_d

# TODO create a python RSA key and show that we can use it to sign

