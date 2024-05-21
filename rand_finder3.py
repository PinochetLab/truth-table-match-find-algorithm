import sys
from itertools import combinations, product


s = '1010010110100101111000010101101001011010010110100001111010100101010110100101101000011110101001010101010101010101000100011010101000100010010001000101010101100110001011010100101101011010011010011101110110111011101010101001100111011101101110111010101010011001010110100101101000011110101001011010010110100101111000010101101001011010010110100001111010100101101010101010101011101110010101011101110110111011101010101001100111011101101110111010101010011001110111011011101110101010100110011101110110111011101010101001100100001111100001110100101100111100111100000111100010110100110000111111000001111000101101001100001111111111011101111011101111001100100010001000100001010101110111011000011110000111010110101101001001110111011101111010101000100010011101110111011110101010001000101111000001111000101101001100001100001111100001110100101100111100111100000111100010110100110000110000000010001000010001000011001101110111011101111010101000100010011101110111011110101010001000100111011101110111101010100010001001110111011101111010101000100010'
mask = '111101111110'
n = mask.count('1')
fst_n = 6
snd_n = 5

array = list(range(n))


def dfs(d):
    d = [(k, d[k]) for k in d]
    values1 = {0: 0}
    values2 = {}
    if _dfs(d, 0, values1, values2):
        return values1, values2
    return None, None


sys.setrecursionlimit(100000)


def _dfs(d, index, values1, values2):
    #print(index, len(d))
    if index >= len(d):
        return True
    _p, ps = d[index]
    i1, i2 = _p
    for v1, v2 in ps:
        if i1 in values1 and v1 != values1[i1]:
            continue
        if i2 in values2 and v2 != values2[i2]:
            continue
        _values1 = dict(values1)
        _values2 = dict(values2)
        _values1[i1] = v1
        _values2[i2] = v2

        if _dfs(d, index + 1, _values1, _values2):
            values1.clear()
            values1.update(_values1)
            values2.clear()
            values2.update(_values2)
            return True
    return False


def transform(values, n):
    array = [0] * (2**n)
    for k in values:
        x = [0] * n
        b = bin(k)[2:]
        for i in range(len(b)):
            if b[len(b) - 1 - i] == '1':
                x[n - 1 - i] = 1
        index = int(''.join([str(v ^ 1) for v in x[::-1]]), 2)
        array[index] = values[k]
    return ''.join([str(v) for v in array])


# Выводим все найденные подпоследовательности
for s1 in list(combinations(array, fst_n)):
    s1 = list(s1)
    s2 = [x for x in array if x not in s1]
    for es in list(combinations(s1, fst_n + snd_n - n)):
        for e in es:
            s2.append(e)
        s2 = sorted(s2)
        #print(s1, s2)
        d = {}
        for x in product((0, 1), repeat=n):
            index = int(''.join([str(v ^ 1) for v in x[::-1]]), 2)
            value = int(s[index])
            i1 = int(''.join([str(x[i]) for i in s1]), 2)
            i2 = int(''.join([str(x[i]) for i in s2]), 2)
            if value:
                ps = ((0, 1), (1, 0))
            else:
                ps = ((0, 0), (1, 1))
            d[(i1, i2)] = ps
        v1, v2 = dfs(d)
        if v1 is not None:
            m = {}
            index = 0
            for i in range(len(mask)):
                if mask[i] == '1':
                    m[index] = i
                    index += 1
            #print(m)
            s1 = [m[i] for i in s1]
            s2 = [m[i] for i in s2]
            print(s1, transform(v1, fst_n))
            print(s2, transform(v2, snd_n))
            exit()
        for e in es:
            s2.remove(e)
