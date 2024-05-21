import itertools
import math
import os
import sys


def transform(i, n):
    b = bin(2**n - 1 - i)[2:]
    return int(('0'*(n - len(b)) + b)[::-1], 2)


def mb(i, n):
    b = bin(i)[2:]
    return '0'*(n - len(b)) + b


def row_to_used(row):
    input_count = int(math.log2(len(row)))
    used = 0
    for i in range(input_count):
        for j in range(1 << i, 2**input_count):
            if (j >> i) & 1 == 0:
                continue
            _inv = j ^ (1 << i)
            if row[transform(j, input_count)] != row[transform(_inv, input_count)]:
                used |= 1 << i
                break
    return used


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
    for (root, _, filenames) in os.walk(folder1):
        print(root)
        for filename in filenames:
            with open(f'{root}/{filename}') as f:
                rows = [list(line.rstrip()) for line in f]
                lines = []
                input_count = int(math.log2(len(rows[0])))
                print(f'processing {filename} {input_count}')
                for i in range(len(rows)):
                    used = row_to_used(rows[i])
                    # print('  --  ', i, mb(used, input_count), end=' ')
                    vc = bin(used)[2:].count('1')
                    r = ""
                    for j in range(2 ** vc):
                        j2 = transform(j, vc)
                        j3 = mask(used, j2, input_count)
                        j4 = transform(j3, input_count)
                        # print(f'({j}->{j2}->{j3}->{j4})', end=' ')
                        r += rows[i][j4]
                    lines.append(mb(used, input_count) + '\t' + r + '\n')
                if not os.path.exists(folder2):
                    os.mkdir(folder2)
                with open(f'{folder2}/{filename}', 'w') as f2:
                    f2.writelines(lines)
