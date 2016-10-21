#!/usr/bin/env python

import gmpy2
import subprocess
from gmpy2 import mpz

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

def string_to_int(tstr):
    # pretty hackish way using encode('hex')
    return int(tstr.encode('hex').replace('L',''),16)

def int_to_string(tint):
    # pretty hackish way using hex()
    unpadded_hex = hex(tint).replace('L','')[2:]
    hex_str = unpadded_hex if len(unpadded_hex) % 2 == 0 else "0"+unpadded_hex
    return hex_str.decode('hex')
