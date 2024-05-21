import math
import os
import sys


def transform(i, n):
    b = bin(2**n - 1 - i)[2:]
    return int(('0'*(n - len(b)) + b)[::-1], 2)


def mb(i, n):
    b = bin(i)[2:]
    return '0'*(n - len(b)) + b


def mask(used, index, n):
    used_s = mb(used, n)
    index_s = mb(index, n)
    result = ['0']*n
    ind = 0
    for i in range(n):
        if used_s[n - 1 - i] == '1':
            result[n - 1 - i] = index_s[n - 1 - ind]
            ind += 1
    return int(''.join(result), 2)


if __name__ == "__main__":
    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    outputs = []

    for (_, _, filenames) in os.walk(folder1):
        for filename in filenames:
            with open(f'{folder1}/{filename}') as f:
                lines = [line.rstrip() for line in f]
                for i in range(len(lines)):
                    split = lines[i].split()
                    used = split[0]
                    row = split[1]
                    vc = used.count('1')
                    if vc <= 1:
                        continue
                    input_count = int(math.log2(len(row)))
                    outputs.append((filename, i, input_count, row))

    for (_, _, filenames) in os.walk(folder2):
        for filename in filenames:
            with open(f'{folder2}/{filename}') as f:
                lines = [line.rstrip() for line in f]
                for i in range(len(lines)):
                    split = lines[i].split()
                    used = split[0]
                    row = split[1]
                    vc = used.count('1')
                    if vc <= 1:
                        continue
                    input_count = int(math.log2(len(row)))
                    one_c = row.count('1')
                    zero_c = 2**input_count - one_c

                    if input_count > 12:
                        continue
                    # m = dict()
                    # sym = True
                    # for i in range(2**input_count):
                    #     oc = bin(transform(i, input_count))[2:].count('1')
                    #     if oc not in m:
                    #         m[oc] = row[i]
                    #     else:
                    #         if m[oc] != row[i]:
                    #             sym = False
                    #if one_c == 1:
                    #    print(f'{folder2}/{filename}({i}) has 1 unit')
                    # if one_c < 4:
                    #     cases = [mb(mask(int(used, 2), k, len(used)), len(used)) for k in range(2**input_count) if row[k] == '1']
                    #     print(f'out({i}) is 1 then {cases}', end=', ')
                    # elif zero_c < 4:
                    #     cases = [mb(mask(int(used, 2), k, len(used)), len(used)) for k in range(2**input_count) if row[k] == '0']
                    #     print(f'out({i}) is 0 then {cases}', end=', ')

                    for fn, out, ic, r in outputs:
                        if ic != input_count:
                            continue
                        m = dict()
                        m['0'] = []
                        m['1'] = []
                        for idx in range(len(r)):
                            m[r[idx]].append(idx)
                        indices = set(range(2 ** input_count))
                        for ind in range(len(row)):
                            c = row[ind]
                            if c not in m:
                                match = False
                                break
                            _indices = set()
                            for j in m[c]:
                                _indices.add(transform(ind, input_count) ^ transform(j, input_count))
                            indices = indices.intersection(_indices)
                            if len(indices) == 0:
                                break
                        if len(indices) > 0:
                            print(f'{folder2}/{filename}({i}) from {folder1}/{fn}({out}) with {mb(list(indices)[0], input_count)}')
                            break
