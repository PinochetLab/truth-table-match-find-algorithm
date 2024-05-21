import sys


if __name__ == '__main__':
    size = int(sys.argv[1])
    filename = str(sys.argv[2])
    s = ""
    for i in range(2**size):
        b = bin(2 ** size - 1 - i)[2:]
        ri = int(('0' * (size - len(b)) + b)[::-1], 2)
        s += '1' if bin(ri)[2:].count('1') > size / 2 else '0'
    print(s)
    with open(filename, 'w') as file:
        file.write(s)
