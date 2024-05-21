import math
import os


def set_char(s, i, a):
    return s[:i] + a + s[i+1:]


def is_sym(line):
    in_count = int(math.log2(len(line)))
    unused = set()
    for i in range(in_count):
        unused.add(i)
        for j in range(2**i, len(line)):
            s = bin(j)[2:]
            ind = len(s) - 1 - i
            if s[ind] == '0':
                continue
            inv = int(s[:ind] + '0' + s[ind+1:], 2)
            if line[j] != line[inv]:
                unused.remove(i)
                break
    print(unused)
    d = dict()
    for i in range(len(line)):
        s = bin(i)[2:]
        count = s.count('1')
        for j in unused:
            if j >= len(s):
                continue
            if s[len(s) - 1 - j] == '1':
                count -= 1
        result = line[i]
        if count not in d:
            d[count] = result
        else:
            if d[count] != result:
                return False
    return True


with open("result3.txt", "w") as file:
    for (_, _, filenames) in os.walk("2024"):
        for filename in filenames:
            with open("2024/" + filename) as f:
                lines = [line.rstrip() for line in f]
                input_count = int(math.log2(len(lines[0])))
                output_count = len(lines)
                sym = True
                syms = []
                for line in lines:
                    syms.append(is_sym(line))
                print(filename, input_count, output_count, syms)
                # file.write(filename + '; ' + str(input_count) + '; ' + str(output_count) + '; ' + str(syms) + '\n')
