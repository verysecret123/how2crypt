#!/usr/bin/env python

import fractions
from Crypto.Util.number import getPrime
from modular_arithmetic import modinv, egcd
from common import yafu, str_to_int, int_to_str, crt, invpow
from rsa import rsa_enc, generate_key
import random

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
    print "In this example we will show how a message can be recovered in low-exponent, unpadded RSA if the it is encrypted using different moduli."
    print ""

    print "This attack requires the usage of the Chinese Remainder Theorem (CRT)."
    print "Given the results of different modulo operations (c_1 = m % n_1, c_2 = m % n_2, ..., c_k = m % c_k) on the same unknown number m, the CRT allows us to recover m if:"
    print "- n_1, n_2, ..., n_k are pairwise coprime"
    print "- m < N where N = n_1 * n_2 * ... * n_k"

    print "Example:"
    n_list = [7,13,19]
    N = reduce(lambda a,b:a*b,n_list,1)
    m = random.randint(100,N)
    print "Let's get three prime moduli %s and m = %d < %d (%s)" % (repr(n_list),m,N,"*".join(map(str,n_list)))
    c_list = []
    for n in n_list:
        c = m % n
        print "%d %% %d == %d" % (m,n,c)
        c_list.append(c)
    recovered_m = crt(c_list,n_list)
    print "original m:", m
    print "recovered m:", recovered_m
    assert m == recovered_m

    print ""
    print "We can use CRT to recover a secret message if:"
    print "- RSA is used without padding"
    print "- a \"small\" exponent is used"
    print "- the same message is encrypted multiple times with different keys"
    print "Given different encrypted messages pow(m,e,n) we use CRT to recover M = pow(m,e) and then we extract the e-th root of M."

    key_length = 1024
    e = 101 # this has to be "small", but it can be bigger than 3
    m = "an extremely secret message!"
    mint = str_to_int(m)
    # longer messages and bigger exponents require more encrypted messages

    print ""
    print "Assuming that the message length is %d, we compute the bit_length of pow(<biggest string of size %d>, e), which is: %d" % (len(m),len(m),(pow(pow(2,len(m) * 8),e).bit_length()))
    print "Every encryption operation uses a modulo whose lower bound is %d bit long" % (key_length-1)
    n_messages = (pow(pow(2,len(m) * 8),e).bit_length() / (key_length-1) ) + 1
    print "So, we need at least (%d/%d) + 1 = %d different encrypted messages to be sure to recover the message" % (pow(pow(2,len(m) * 8),e).bit_length(),(key_length-1),n_messages)

    n_list = []
    c_list = []
    for _ in xrange(n_messages):
        p,q,d = generate_key(key_length, e)
        n = p*q
        # during every encryption step pow(m,e) is always the same "unknown" value, whereas n changes
        c = rsa_enc(mint, e, n)
        n_list.append(n)
        c_list.append(c)
    recovered_pow_m_e = crt(c_list,n_list)

    recovered_message = int_to_str(invpow(recovered_pow_m_e,e))
    print ""
    print "original message:", repr(m)
    print "recovered message:", repr(recovered_message)
    assert m == recovered_message
