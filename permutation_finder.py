import itertools
import math
import os


m = dict()

for (_, _, filenames) in os.walk("2023"):
    for filename in filenames:
        with open("2023/" + filename) as f:
            lines = [list(line.rstrip()) for line in f]
            input_count = int(math.log2(len(lines[0])))
            content = '_'.join([''.join(line) for line in lines])
            m[input_count, content] = filename


# for (_, _, filenames) in os.walk("2024"):
#     for filename in filenames:
#         with open("2024/" + filename) as f:
#             lines = [list(line.rstrip()) for line in f]
#             input_count = int(math.log2(len(lines[0])))
#             if input_count > 12:
#                 continue
#             print(f'\nprocessing {filename} {input_count}')
#             for i in range(0, 2**input_count):
#                 # print(i)
#                 _lines = [[line[j ^ i] for j in range(len(line))] for line in lines]
#                 _content = '_'.join([''.join(line) for line in _lines])
#                 if _content in m:
#                     print(f'{m[input_count, _content]} -> {filename}')


for (_, _, filenames) in os.walk("2024"):
    for filename in filenames:
        with open("2024/" + filename) as f:
            lines = [list(line.rstrip()) for line in f]
            input_count = int(math.log2(len(lines[0])))
            if input_count > 9:
                continue
            print(f'\nprocessing permutations {filename} {input_count}')
            perm = [0] * (2**input_count)
            for p in itertools.permutations(list(range(input_count))):
                # print(p)
                for i in range(0, 2 ** input_count):
                    b = bin(i)[2:]
                    s = '0'*(input_count - len(b)) + b
                    s2 = ''
                    for j in range(input_count):
                        s2 += s[p[j]]
                    perm[i] = int(s2, 2)
                # print(i)
                _lines = [[line[perm[j]] for j in range(len(line))] for line in lines]
                _content = '_'.join([''.join(line) for line in _lines])
                if _content in m:
                    print(f'{m[input_count, _content]} -> {filename}')

