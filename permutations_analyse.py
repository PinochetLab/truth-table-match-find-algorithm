import math
from itertools import product, permutations

def transform(i, n):
    b = bin(2**n - 1 - i)[2:]
    return int(('0'*(n - len(b)) + b)[::-1], 2)

orig = '1000100000000000000000000000000011011111000000001000101000000000'

n = int(math.log2(len(orig)))
s = set()

for permutation, negations in product(permutations(range(n)), product((0, 1), repeat=n)):
    st = ""
    for x in list(product((0, 1), repeat=n))[::-1]:
        x = x[::-1]
        x = [x[permutation[i]] ^ negations[i] ^ 1 for i in range(n)][::-1]
        st += orig[int(''.join([str(k) for k in x]), 2)]
    print(st)
    s.add(st)
print(len(s), math.factorial(n) * 2**n)

