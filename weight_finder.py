import itertools
import math
import re


bench_path = ""


class Node:
    def __init__(self, name: str):
        self.name = name

    def eval(self, values: dict[str, int]) -> int:
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()


class Lit(Node):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name

    def eval(self, values: dict[str, int]) -> int:
        return values[self.name]

    def __repr__(self):
        return self.name


class Not(Node):
    def __init__(self, name: str, child: Node):
        super().__init__(name)
        self.child = child

    def eval(self, values: dict[str, int]) -> int:
        return not self.child.eval(values)

    def __repr__(self):
        return f'{self.name}=Not({self.child.name})'


class And(Node):
    def __init__(self, name: str, left: Node, right: Node):
        super().__init__(name)
        self.left = left
        self.right = right

    def eval(self, values: dict[str, int]) -> int:
        return self.left.eval(values) and self.right.eval(values)

    def __repr__(self):
        return f'{self.name}=And({self.left.name}, {self.right.name})'


class Or(Node):
    def __init__(self, name: str, left: Node, right: Node):
        super().__init__(name)
        self.left = left
        self.right = right

    def eval(self, values: dict[str, int]) -> int:
        return self.left.eval(values) or self.right.eval(values)

    def __repr__(self):
        return f'{self.name}=Or({self.left.name}, {self.right.name})'


class Xor(Node):
    def __init__(self, name: str, left: Node, right: Node):
        super().__init__(name)
        self.left = left
        self.right = right

    def eval(self, values: dict[str, int]) -> int:
        return self.left.eval(values) ^ self.right.eval(values)

    def __repr__(self):
        return f'{self.name}=Xor({self.left.name}, {self.right.name})'


def parse(path: str) -> tuple[list[str], list[Node]]:
    inputs = []
    saved_nodes = dict()
    with open(path) as file:
        lines = [line.rstrip() for line in file]
        for line in lines:
            input_pattern = r'INPUT\((.*?)\)'
            input_result = re.search(input_pattern, line)
            if input_result:
                input_name = input_result.group(1)
                input_node = Lit(input_name)
                saved_nodes[input_name] = input_node
                inputs.append(input_name)
            else:
                output_pattern = r'OUTPUT\((.*?)\)'
                output_result = re.search(output_pattern, line)
                if output_result:
                    pass
                else:
                    formula_pattern = r'(\w+)=(\w+)\(([^)]*)\)'
                    new_line = line.replace(' ', '')
                    formula_result = re.search(formula_pattern, new_line)
                    if formula_result:
                        lit = formula_result.group(1)
                        operation = formula_result.group(2)
                        operands = formula_result.group(3).split(',')
                        if operation == 'NOT':
                            node = Not(lit, saved_nodes[operands[0]])
                        elif operation == 'AND':
                            node = And(lit, saved_nodes[operands[0]], saved_nodes[operands[0]])
                        elif operation == 'OR':
                            node = Or(lit, saved_nodes[operands[0]], saved_nodes[operands[0]])
                        elif operation == 'XOR':
                            node = Xor(lit, saved_nodes[operands[0]], saved_nodes[operands[0]])
                        else:
                            print(operation)
                            raise NotImplementedError()
                        saved_nodes[lit] = node
    return inputs, list(saved_nodes.values())


def parse_table(path: str) -> list[int]:
    with open(path) as file:
        lines = [line.rstrip() for line in file]
        return [int(v) for v in lines[0]]


inputs, nodes = parse('google_maj.bench')

weights = [1, 2, 2, 2, 2]
n = len(weights)

table = parse_table('files/maj9.truth')
size = int(math.log2(len(table)))

for ns in itertools.combinations(nodes, n):
    good = True
    for x in itertools.product((0, 1), repeat=size):
        s = sum(x)
        values = dict()
        for i in range(len(x)):
            values[inputs[i]] = x[i]
        nodes_values = [node.eval(values) for node in ns]
        _s = sum([nodes_values[i] * weights[i] for i in range(len(nodes_values))])
        if s != _s:
            good = False
            break
    if good:
        print(f'weights: {weights}')
        print(f'  gates: {[node.name for node in ns]}')
        break
