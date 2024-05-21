from itertools import combinations, product


s = '1011101011000111010001010011100001000101001110000001000001101101100110100011001001100101110011010110010111001101001100001001100011101111100100100001000001101101000100000110110110111010110001111100111101100111001100001001100000110000100110001001101000110010'

# Исходный массив из 9 элементов
array = [0, 1, 2, 3, 4, 5, 6, 7]

# Находим все комбинации из 5 элементов
subsequences = list(combinations(array, 5))


def dfs(d):
    d = [(k, d[k]) for k in d]
    values1 = {0: 0}
    values2 = {}
    if _dfs(d, 0, values1, values2):
        return values1, values2
    return None, None


def _dfs(d, index, values1, values2):
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
for s1 in list(combinations(array, 5)):
    s1 = list(s1)
    s2 = [x for x in array if x not in s1]
    for e in s1:
        s2.append(e)
        s2 = sorted(s2)
        d = {}
        for x in product((0, 1), repeat=8):
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
            mask = '1110101111'
            m = {}
            index = 0
            for i in range(10):
                if mask[i] == '1':
                    m[index] = i
                    index += 1
            s1 = [m[i] for i in s1]
            s2 = [m[i] for i in s2]
            print(s1, transform(v1, 5))
            print(s2, transform(v2, 4))
            exit()

        s2.remove(e)
