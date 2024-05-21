import math
import os


def transform(i, n):
    b = bin(2**n - 1 - i)[2:]
    return int(('0'*(n - len(b)) + b)[::-1], 2)


def mb(i, n):
    b = bin(i)[2:]
    return '0'*(n - len(b)) + b


for _, _, filenames in os.walk("2023s"):
    for filename in filenames:
        with open("2023s/" + filename) as f:
            lines = [line.rstrip() for line in f]

            if filename != 'ex49.truth':
                continue
            print(f'processing {filename}')
            majority = []

            index = 0
            for line in lines:
                split = line.split()
                mask = split[0]
                row = split[1]
                input_count = int(math.log2(len(row)))
                m = False
                for inv in range(2**input_count):
                    maj = True
                    inv_c = bin(inv)[2:].count('1')
                    for i in range(2**input_count):
                        one_c = bin(i ^ inv)[2:].count('1')
                        # print(filename, i, input_count, 2**input_count, transform(i, input_count), len(row))
                        if (row[transform(i, input_count)] == '1') != (one_c > input_count // 2):
                            maj = False
                            break

                    unused = 2**input_count - 1
                    if maj:
                        inv_s = bin(inv)[2:]
                        inv_s = '0' * (input_count - len(inv_s)) + inv_s
                        unused_s = bin(unused)[2:]
                        unused_s = '0' * (input_count - len(unused_s)) + unused_s
                        result = ['0' if unused_s[i] == '0' else ('1' if inv_s[i] == '0' else '-1') for i in
                                  range(input_count)]
                        s = ""
                        ind = 0
                        for k in range(input_count):
                            while mask[len(mask) - 1 - ind] != '1':
                                ind += 1
                            if result[input_count - 1 - k] == '-1':
                                s += '-' if len(s) == 0 else ' - '
                                s += f'x_{ind}'
                            else:
                                s += '' if len(s) == 0 else ' + '
                                s += f'x_{ind}'
                            ind += 1
                        s = f'Maj_{input_count} [{s} > {input_count // 2 - inv_c}]'
                        print(index, s)

                        m = True
                        break
                majority.append('Y' if m else 'N')
                index += 1
            print(majority)
