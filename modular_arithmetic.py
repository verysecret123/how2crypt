#!/usr/bin/env python

import random

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b / a) * y, y)

def modinv(a, n):
    g, x, y = egcd(a, n)
    if g != 1:
        raise Exception('modular inverse (%d, %d) does not exist' % (a, n))
    else:
        return x % n

if __name__ == '__main__':
    print "Let's see some basic modular arithmetic!"
    print "People that actually know math: please forgive me :-)"
    print ""

    print "The modulo can be computed as the remainder of a division or using the Python % operator"
    print "remember that in Python2 the operator / when used with integers is the integer division (so remainder is truncated)"
    print "more conveniently, you can use the operator % to compute modulo"
    for _ in xrange(3):
        a = random.randint(1,30)
        b = random.randint(1,30)
        print "{a} - (({a}/{b})*{b}) == {a} % {b} == {res}".format(a=a,b=b,res=(a%b))

    print "frequently the notation a=b (mod n) is used, what it means is just a%n=b%n"
    print ""

    print "In Python (pow(a,b)) % n can be computed by passing three arguments to the funciton pow: pow(a,b) % n == pow(a,b,n)"
    print "Some properties of modular arithmetic:"
    print "- (a * b) % n == ((a % n) * (b % n)) % n"
    print "- pow(a,b,n) == pow(a%n,b,n)"
    print "however pow(a,b,n) is not always equal to pow(a,b%n,n) when b > n (we will see later how to use the totient to \"apply the modulo to the exponent\")"
    print "Examples:"
    for _ in xrange(8):
        a = random.randint(1,100)
        b = random.randint(1,100)
        n = random.randint(1,100)
        print "a={a}, b={b}, n={n}".format(n=n,a=a,b=b)
        print "({a}*{b})%n == {ab1} == {ab2} == (({a}%{n})*({b}%{n}))%{n}".format(n=n,a=a,b=b,ab1=(a*b)%n,ab2=((a%n)*(b%n))%n)
        print "pow({a},{b},{n}) == {pow1} == {pow2} == pow({a}%{n},{b},{n})".format(n=n,a=a,b=b,pow1=pow(a,b,n),pow2=pow(a%n,b,n))
        print "pow({a},{b},{n}) == {pow1} not always equal to {pow2} == pow({a},{b}%{n},{n})".format(n=n,a=a,b=b,pow1=pow(a,b,n),pow2=pow(a,b%n,n))
        print "-"*25

    print "One important concept in modular arithmetic is the totient (phi)"
    print "Formally the totient k = phi(n) is the number of integers k in the range 1 <= k <= n for which the greatest common divisor GCD(n,k) = 1 (in other words, n is coprime with k)"

    # for now let's use the "standard" GCD imported from fractions
    from fractions import gcd
    def phi(n,debug=False):
        tot = 0
        coprime = []
        for i in xrange(1,n+1):
            if gcd(i,n) == 1:
                tot += 1
                if debug:
                    coprime.append(i)

        if not debug:
            return tot
        else:
            return tot,coprime

    print "Let's compute some totients"
    for _ in xrange(3):
        n = random.randint(1,30)
        t,coprimes = phi(n,debug = True)
        print "phi({n}) == {t} (these are the {len} coprimes: {coprimes})".format(n=n,t=t,len=len(coprimes),coprimes=coprimes)
    print "It is important to notice that:"
    print "- if n is a prime number phi(n) == n-1 and t"
    print "- phi(a*b) = phi(a) * phi(b)"

    print "Examples:"
    def get_prime(pmin=10,pmax=100):
        #very inefficient way to get a prime
        tlist = range(pmin,pmax+1)
        random.shuffle(tlist)
        for i in tlist:
            for j in xrange(2,(i/2)+2):
                if i % j == 0:
                    break
            else:
                return i

    for _ in xrange(3):
        p = get_prime()
        print "phi({p}) == {phi}".format(p=p,phi=phi(p))
    for _ in xrange(3):
        a = random.randint(1,100)
        b = random.randint(1,100)
        print "phi({a}*{b}) == {phi_a} * {phi_b} == {phi_ab} == phi({ab})".format(a=a,b=b,ab=a*b,phi_ab=phi(a*b),phi_a=phi(a),phi_b=phi(b))
    print ""

    print "One important properties (Euler theorem) is the following:"
    print "pow(a,phi(n),n) == 1 <==> gcd(a,n)==1"
    print "As a consequence of the Euler theorem: if gcd(a,n) == 1, pow(a,b,n) == pow(a,b % phi(n),n)"
    print "Examples:"
    i = 0
    while i<3:
        a = random.randint(1,100)
        b = random.randint(1,100)
        n = random.randint(1,100)
        if gcd(a,n) != 1 or a>n or b>n:
            continue
        i += 1
        print "a={a}, n={n}, gcd(a,n) = {gcd}, phi({n})={phi}, pow({a},{phi},{n}) == {ppow}".format(a=a,n=n,gcd=gcd(a,n),phi=phi(n),ppow=pow(a,phi(n),n))
        print "b={b}, b%n={bmod}, pow({a},{b},{n}) == {res} ==  pow({a},{bmod},{n}) == pow({a},{b}%phi({n}),{n})".format(a=a,b=b,n=n,bmod=b%n,res=pow(a,b%phi(n),n))
    print ""

    print "The modular inverse d of e mod n is a number d such that (e*d)%n == 1"
    print "There is an easy algorithm to find it"

    def egcd(a, b):
        # this is the "extended" version of the gcd
        # given two numbers a and b, it returns the triple (g, x, y) such that ax + by = g = gcd(a, b)
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

    print "please note that the modular inverse of a in modulo n only exists if gcd(a,n) == 1"
    for _ in xrange(8):
        a = random.randint(1,100)
        n = random.randint(1,100)
        print "a={a}, n={n}, gcd(a,n) == {gcd}, modinv(a,n) == {inv}".format(a=a,n=n,gcd=gcd(a,n),inv=repr(modinv(a,n)))
    print ""

    print "Finally, if gcd(e,phi(n)) == 1 and pow(x,e,n) = y, y can assume all the n values between 0 and n-1"
    print "otherwise, if  gcd(e,phi(n)) != 1, y can assume only a subset of those values"

    for _ in xrange(8):
        e = random.randint(2,20)
        n = random.randint(1,20)
        yset = set()
        for i in xrange(n):
            yset.add(pow(i,e,n))
        print "e={e}, n={n}, gcd(e,n)={gcd}, len(yset) = {lset}, yset = {yset}".format(e=e,n=n,gcd=gcd(e,n),lset=len(yset),yset=sorted(yset)),
        if gcd(e,n)==1:
            print "--> n == len(yset) since gcd(e,n) == 1"
        else:
            print ""
    print ""

    print "If gcd(e,phi(n)) == 1, the function f(x) = pow(x,e,n) maps every number in the set(range(0,n)) to another distinct number within the same set"
    print "In addition, the function g(x) = pow(x,modinv(e,phi(n)),n) is the inverse of f(x), so that g(f(x)) == x"
    while True:
        e = random.randint(10,25)
        n = random.randint(10,25)
        if gcd(e,phi(n))==1 and n > e:
            break
    ph = phi(n)
    inv = modinv(e,ph)
    print "e={e}, n={n}, ph={ph}, modinv(e,phi(n))={inv}".format(e=e,n=n,ph=ph,inv=inv)
    for x in xrange(n):
        print "x={x}, pow(x,e,n) == {ppow}, pow({ppow},modinv(e,phi(n)),n) == {res}".format(x=x,ppow=pow(x,e,n),res=pow((pow(x,e,n)),modinv(e,phi(n)),n))

