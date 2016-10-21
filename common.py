#!/usr/bin/env python

import gmpy2
import subprocess
from gmpy2 import mpz
from modular_arithmetic import modinv

def little_factors(n):
    result = set()
    n = mpz(n)
    for i in range(1, gmpy2.isqrt(n) + 1):
        div, mod = divmod(n, i)
        if not mod:
            result |= {mpz(i), div}
    return map(int, result)

def yafu(n):
    output, errput = subprocess.Popen([ 'yafu', 'factor(%d)' % n], stdout=subprocess.PIPE).communicate()
    primes = [ int(line.split(" ")[-1]) for line in output.split('\n') if line.startswith("P") ]
    return primes

def str_to_int(tstr):
    # pretty hackish way using encode('hex')
    return int(tstr.encode('hex').replace('L',''),16)

def int_to_str(tint):
    # pretty hackish way using hex()
    unpadded_hex = hex(tint).replace('L','')[2:]
    hex_str = unpadded_hex if len(unpadded_hex) % 2 == 0 else "0"+unpadded_hex
    return hex_str.decode('hex')

def crt(a,n):
    # from http://rosettacode.org/wiki/Chinese_remainder_theorem#Python
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * modinv(p, n_i) * p
    return sum % prod

def invpow(x,n):
    # from: http://stackoverflow.com/questions/356090/how-to-compute-the-nth-root-of-a-very-big-integer
    """Finds the integer component of the n'th root of x,
    an integer such that y ** n <= x < (y + 1) ** n.
    """
    high = 1
    while high ** n < x:
        high *= 2
    low = high/2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1
 