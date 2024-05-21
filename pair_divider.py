import copy
import itertools
import math


def get_pairs(row):
    n = int(math.log2(len(row)))
    pairs = {}
    for i in range(n):
        for val in (0, 1):
            for j in range(n):
                if j == i:
                    continue
                depends = False
                for x in itertools.product((0, 1), repeat=n):
                    if x[i] != val:
                        continue
                    x = list(x)
                    index1 = int(''.join([str(v ^ 1) for v in x[::-1]]), 2)
                    x[j] ^= 1
                    index2 = int(''.join([str(v ^ 1) for v in x[::-1]]), 2)
                    if i == 1 and j == 15 and x == (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1):
                        print(row[index1])
                        print(row[index2])
                    if row[index1] != row[index2]:
                        depends = True
                        break
                if not depends:
                    if j in pairs:
                        pairs[j].append(val)
                    else:
                        pairs[i] = [j, val]
                    break
    return pairs


with open('2024/ex55.truth') as f:
    row = [line.rstrip() for line in f][0]
    n = int(math.log2(len(row)))
    ps = get_pairs(row)
    print(ps)

    class Node:
        def evaluate(self, values, negations):
            raise NotImplementedError()

    class Op(Node):
        def __init__(self, op, left: Node, right: Node):
            self.op = op
            self.left = left
            self.right = right

        def evaluate(self, values, negations):
            neg = negations[0]
            #print(neg, self.__str__())
            ns = negations[1:]
            left_val = self.left.evaluate(values, ns[:len(ns) // 2])
            right_val = self.right.evaluate(values, ns[len(ns) // 2:])
            if self.op == 'and':
                val = left_val & right_val
            else:
                val = left_val ^ right_val
            return val ^ neg

        def __str__(self):
            return f'{self.op}({self.left.__str__(), self.right.__str__()})'

    class Lit(Node):
        def __init__(self, index, negation):
            self.index = index
            self.negation = negation

        def evaluate(self, values, negations):
            return values[self.index] ^ self.negation

        def __str__(self):
            return f'{"!" if self.negation else ""}x{self.index}'

    nodes = []
    for i in ps:
        j, v1, v2 = ps[i]
        nodes.append(Op('and', Lit(i, v1), Lit(j, v2)))

    for p in itertools.permutations(nodes):
        node = Op('xor', Op('and', Op('xor', p[0], p[1]), Op('xor', p[2], p[3])),
                             Op('and', Op('xor', p[4], p[5]), Op('xor', p[6], p[7])))

        print([nodes.index(x) for x in p])

        for negations in itertools.product((0, 1), repeat=n-1):
            if negations != (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0):
                continue
            #print(negations)
            success = True
            for x in itertools.product((0, 1), repeat=n):
                index = int(''.join([str(v ^ 1) for v in x[::-1]]), 2)
                value = node.evaluate(list(x), list(negations))
                #print(value)
                if int(row[index]) != value:
                    #print(x, value, row[index])
                    success = False
                    break
            if success:
                print(negations)
                exit()
            #exit()
