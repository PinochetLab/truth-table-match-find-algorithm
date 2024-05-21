import math
import sys

# from is_majority import transform

if __name__ == "__main__":
    orig = str(sys.argv[1])
    new = str(sys.argv[2])
    lines = []
    with open(orig) as f:
        rows = [list(line.rstrip()) for line in f]
        input_count = int(math.log2(len(rows[0])))
        length = 1 << input_count
        for row in rows:
            line = ""
            for i in range(length):
                # j = transform(i, input_count)
                b = bin(2 ** input_count - 1 - i)[2:]
                j = int(('0' * (input_count - len(b)) + b)[::-1], 2)
                line += row[j]
            lines.append(line + "\n")
            # print("line:", line)
        with open(new, 'w') as file:
            file.writelines(lines)

