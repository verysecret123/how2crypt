#!/usr/bin/env python

import fractions
from Crypto.Util.number import getPrime
from modular_arithmetic import modinv, egcd
from common import yafu

def rsa_enc(m, e, n):
    return pow(m, e, n)

def rsa_dec(c, d, n):
    return pow(c, d, n)

def generate_key(bits, e):
    """
    Returns p and q.
    """
    p = getPrime(bits/2)
    q = getPrime(bits/2)

    if fractions.gcd(p-1, e) != 1 or fractions.gcd(q-1, e) != 1:
        return generate_key(bits, e)
    else:
        return p, q, modinv(e, (p-1)*(q-1))

if __name__ == '__main__':
    print "Welcome to RSA 4 noobs!"
    print
    print "Generating an RSA key."

    e = 3
    p,q,d = generate_key(128, e)
    n = p*q
    print "... p:", p
    print "... q:", q
    print "... d:", d
    print "... n:", p*q
    print "... fi(n):", (p-1)*(q-1)

    print
    print "Encryption demo:"
    m = int("hello".encode('hex'), 16)
    print "... message:", m
    c = rsa_enc(m, e, n)
    print "... encrypted:", c
    print "... decrypted:", rsa_dec(c, d, n)

    print "#"
    print "# Common RSA attacks:"
    print "#"
    print
    print "Let's do the naive attack of factoring primes."
    p,q = yafu(n)
    print "... factors of n:", (p,q)
    print "Now, we can compute our own d (private key)."
    attacker_fi = (p-1)*(q-1)
    print "... attacker computed fi:", attacker_fi
    attacker_d = modinv(e, attacker_fi)
    print "... attacker computed d:", attacker_d
    print "... attacker decrypted message:", pow(c, attacker_d, n)

    print
    print "Next, let's demonstrate the problem of having a small exponent e."
    print "If we have a small message, the ciphertext won't \"wrap around\", and the modulus won't do anything."
    m = int("Hi".encode('hex'), 16)
    print "For example, let's say that our message is %d." % m
    c = pow(m, e, n)
    print "This encrypts to %d without wrapping around %d." % (c, n)
    print "Now, instead of using the exponent, we can simply take the (non-modular) cube root.", c**(1./3)

    print ""
    print "Those are some naive attacks against unpadded, simple RSA. See other files for other attacks."

# TODO rsa stuff
# show how to manually do rsa with modular pow and phi
# explain encypt/decrypt/sign
# message to number and number to message
# padded/unpadded RSA
# show how to import/export stuff from/to Crypto.PublicKey RSA
# show CRT and how CRT is saved in ssh private keys
