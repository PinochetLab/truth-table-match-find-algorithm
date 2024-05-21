import itertools
import math
import os


def transform(i, n):
    b = bin(2**n - 1 - i)[2:]
    return int(('0'*(n - len(b)) + b)[::-1], 2)


def mb(i, n):
    b = bin(i)[2:]
    return '0'*(n - len(b)) + b


tables = []

for (_, _, filenames) in os.walk("2023"):
    for filename in filenames:
        with open("2023/" + filename) as f:
            m = dict()
            rows = [list(line.rstrip()) for line in f]
            input_count = int(math.log2(len(rows[0])))
            output_count = len(rows)
            columns = list(map(''.join, zip(*rows)))
            for i in range(len(columns)):
                c = columns[i]
                if c not in m:
                    m[c] = [i]
                else:
                    m[c].append(i)
            tables.append((filename, input_count, output_count, rows))


for (_, _, filenames) in os.walk("2024"):
    for filename in filenames:
        with open("2024/" + filename) as f:
            rows = [list(line.rstrip()) for line in f]
            input_count = int(math.log2(len(rows[0])))
            output_count = len(rows)
            if input_count > 10:
                continue
            print(f'processing {filename} {input_count} {output_count}')
            columns = list(map(''.join, zip(*rows)))
            ma = {}
            for i in range(len(columns)):
                c = columns[i]
                if c not in ma:
                    ma[c] = [i]
                else:
                    ma[c].append(i)

            for fn, in_c, out_c, rs in tables:
                # print('fn', fn, in_c, out_c)
                # if input_count != in_c or output_count != out_c:
                #     continue
                # b = True
                # for c in ma:
                #     arr = ma[c]
                #     if c not in m:
                #         b = False
                #         break
                #     if len(arr) != len(m[c]):
                #         b = False
                #         break
                # if b:
                #     print(f'{filename} maybe from {fn}')

                if input_count != in_c or output_count != out_c:
                    continue

                # print(f'  maybe from {fn}?')

                for k1 in range(len(rows)):
                    for k2 in range(len(rows)):
                        f = False
                        for inv in range(2 ** input_count):
                            align = True
                            for i in range(2 ** input_count):
                                j = i ^ inv
                                if rows[k1][transform(i, in_c)] != rs[k2][transform(j, in_c)]:
                                    align = False
                                    break
                            if align:
                                print(f' --- out({k1}) from {fn}({k2}) with inv={mb(inv, in_c)}')
                                f = True
                                break
                        if f:
                            break


                # print(f'{filename} from {fn}')
                # indices = set(range(2**input_count))
                # match = True
                # for i in range(len(columns)):
                #     c = columns[i]
                #     if c not in m:
                #         match = False
                #         break
                #     _indices = set()
                #     for j in m[c]:
                #         _indices.add(transform(i, input_count) ^ transform(j, input_count))
                #     # exit(0)
                #     indices = indices.intersection(_indices)
                #     # print(fn, filename, i, c, len(indices))
                #     if len(indices) == 0:
                #         match = False
                #         break
                # if match:
                #     print(f'from {fn}')
                #     break
