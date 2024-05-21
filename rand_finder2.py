import sys
from itertools import combinations, product


s = '1001011000001111100110101011110001110000101100101011000001101011101001000011101110110110111110111010101010101001110101011011011001001101000010011000001001100110100001110011011000101000010101010010001101111001000010000000111010101011000100011100011010111101111001010000010110101100111001101101111011011000001100110001001010110000110000101101110100001001100000001001010000111010010000010110111111111110001110000111101001110111111001011000001001110101011000111011011010110001101001011011101011100111010111010101000100001100100101010010101111010110000100111111011100110010010011110100000010000000011100000111110110011010000101111000100001010111100011010100001101101001110111011110101100110001001000001000010000011000010011000100110000001101111110000100101111000010111011111101000011111111001111110010010000000010101000000100110000001110010000011000011011101010001010011011111111010001111010011101111100110111111010010001001010000011010010100101000100000100111010011111111110001100101110101010010000110100111010111010001101110010'

# Исходный массив из 9 элементов
array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Находим все комбинации из 5 элементов
subsequences = list(combinations(array, 5))


def dfs(d):
    d = [(k, d[k]) for k in d]
    values1 = {0: 0}
    values2 = {}
    if _dfs(d, 0, values1, values2):
        return values1, values2
    return None, None


sys.setrecursionlimit(1050)


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
for s1 in list(combinations(array, 6)):
    s1 = list(s1)
    s2 = [x for x in array if x not in s1]
    for e in s1:
        s2.append(e)
        s2 = sorted(s2)
        #print(s1, s2)
        d = {}
        for x in product((0, 1), repeat=10):
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
            mask = '111101111110'
            m = {}
            index = 0
            for i in range(12):
                if mask[i] == '1':
                    m[index] = i
                    index += 1
            #print(m)
            s1 = [m[i] for i in s1]
            s2 = [m[i] for i in s2]
            print(s1, transform(v1, 6))
            print(s2, transform(v2, 5))
            exit()

        s2.remove(e)
