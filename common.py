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
