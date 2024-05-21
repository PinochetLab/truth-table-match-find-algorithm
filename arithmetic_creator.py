import math
import os
from itertools import product
from typing import Callable


folder = 'arithmetics/'


def write_in_file(matrix: list[list[int]], path: str, name: str):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + name, 'w') as file:
        for line in matrix:
            file.write(''.join(map(str, line)) + '\n')


def create_matrix() -> list[list[int]]:
    return []


def to_index(x: list[int]) -> int:
    return int(''.join(map(str, x)), 2)


def to_transformed_index(x: list[int]) -> int:
    return int(''.join([str(v ^ 1) for v in x[::-1]]), 2)


def write_column(matrix: list[list[int]], n: int, index: int, number: int):
    array = list(map(int, list(bin(number)[2:])))[::-1]
    for i in range(len(array)):
        while i >= len(matrix):
            matrix.append([0] * (2 ** n))
        matrix[i][index] = array[i]


def create_f2_matrix(f2: Callable[[int, int], int], n1: int, n2: int) -> list[list[int]]:
    matrix = create_matrix()
    for x in product((0, 1), repeat=n1 + n2):
        i1 = to_index(x[:n1])
        i2 = to_index(x[n1:])
        mul = f2(i1, i2)
        index = to_transformed_index(x)
        write_column(matrix, n1 + n2, index, mul)
    return matrix


def create_f1_matrix(f1: Callable[[int], int], n: int) -> list[list[int]]:
    matrix = create_matrix()
    for x in product((0, 1), repeat=n):
        i = to_index(x)
        mul = f1(i)
        index = to_transformed_index(x)
        write_column(matrix, n, index, mul)
    return matrix


def create_mul(n1: int, n2: int):
    def mul(i1: int, i2: int) -> int:
        return i1 * i2
    matrix = create_f2_matrix(mul, n1, n2)
    write_in_file(matrix, folder + '/mult/', f'mult_{n1}_{n2}.truth')


def create_sum(n1: int, n2: int):
    def sum(i1: int, i2: int) -> int:
        return i1 + i2
    matrix = create_f2_matrix(sum, n1, n2)
    write_in_file(matrix, folder + '/sum/', f'sum_{n1}_{n2}.truth')


def create_div(n1: int, n2: int):
    def div(i1: int, i2: int) -> int:
        if i2 == 0:
            return 0
        return i1 // i2
    matrix = create_f2_matrix(div, n1, n2)
    write_in_file(matrix, folder + '/div/', f'div_{n1}_{n2}.truth')


def create_mod(n1: int, n2: int):
    def mod(i1: int, i2: int) -> int:
        if i2 == 0:
            return i2
        return i1 % i2
    matrix = create_f2_matrix(mod, n1, n2)
    write_in_file(matrix, folder + '/mod/', f'mod_{n1}_{n2}.truth')


def create_pow(n1: int, n2: int):
    def pow(i1: int, i2: int) -> int:
        return i1 ** i2
    matrix = create_f2_matrix(pow, n1, n2)
    write_in_file(matrix, folder + '/pow/', f'pow_{n1}_{n2}.truth')


def create_greater(n1: int, n2: int):
    def greater(i1: int, i2: int) -> int:
        return i1 > i2
    matrix = create_f2_matrix(greater, n1, n2)
    write_in_file(matrix, folder + '/greater/', f'greater_{n1}_{n2}.truth')


def create_equal(n1: int, n2: int):
    def equal(i1: int, i2: int) -> int:
        return i1 == i2
    matrix = create_f2_matrix(equal, n1, n2)
    write_in_file(matrix, folder + '/equal/', f'equal_{n1}_{n2}.truth')


def create_abs_sub(n1: int, n2: int):
    def abs_sub(i1: int, i2: int) -> int:
        return int(math.fabs(i1 - i2))
    matrix = create_f2_matrix(abs_sub, n1, n2)
    write_in_file(matrix, folder + '/abs_sub/', f'abs_sub_{n1}_{n2}.truth')


def create_gcd(n1: int, n2: int):
    def gcd(i1: int, i2: int) -> int:
        return math.lcm(i1, i2)
    matrix = create_f2_matrix(gcd, n1, n2)
    write_in_file(matrix, folder + '/gcd/', f'gcd_{n1}_{n2}.truth')


def create_lcm(n1: int, n2: int):
    def lcm(i1: int, i2: int) -> int:
        return math.lcm(i1, i2)
    matrix = create_f2_matrix(lcm, n1, n2)
    write_in_file(matrix, folder + '/lcm/', f'lcm_{n1}_{n2}.truth')


def create_max(n1: int, n2: int):
    def f(i1: int, i2: int) -> int:
        return max(i1, i2)
    matrix = create_f2_matrix(f, n1, n2)
    write_in_file(matrix, folder + '/max/', f'max_{n1}_{n2}.truth')


def create_min(n1: int, n2: int):
    def f(i1: int, i2: int) -> int:
        return min(i1, i2)
    matrix = create_f2_matrix(f, n1, n2)
    write_in_file(matrix, folder + '/min/', f'min_{n1}_{n2}.truth')


def create_log_a_b(n1: int, n2: int):
    def f(i1: int, i2: int) -> int:
        return int(math.log(i1 + 1, i2))
    matrix = create_f2_matrix(f, n1, n2)
    write_in_file(matrix, folder + '/log_a_b/', f'log_a_b_{n1}_{n2}.truth')


def create_sqr(n: int):
    def sqr(i: int) -> int:
        return i ** 2
    matrix = create_f1_matrix(sqr, n)
    write_in_file(matrix, folder + '/sqr/', f'sqr_{n}.truth')


def create_sqrt(n: int):
    def sqrt(i: int) -> int:
        return int(math.sqrt(i))
    matrix = create_f1_matrix(sqrt, n)
    write_in_file(matrix, folder + '/sqrt/', f'sqrt_{n}.truth')


def create_cbrt(n: int):
    def f(i: int) -> int:
        return int(math.cbrt(i))
    matrix = create_f1_matrix(f, n)
    write_in_file(matrix, folder + '/cbrt/', f'cbrt_{n}.truth')


def create_log(n: int):
    def f(i: int) -> int:
        return int(math.log(1 + i))
    matrix = create_f1_matrix(f, n)
    write_in_file(matrix, folder + '/log/', f'log_{n}.truth')


def create_log2(n: int):
    def f(i: int) -> int:
        return int(math.log2(1 + i))
    matrix = create_f1_matrix(f, n)
    write_in_file(matrix, folder + '/log2/', f'log2_{n}.truth')


def create_log10(n: int):
    def f(i: int) -> int:
        return int(math.log10(1 + i))
    matrix = create_f1_matrix(f, n)
    write_in_file(matrix, folder + '/log10/', f'log10_{n}.truth')


def create_add_one(n: int):
    def f(i: int) -> int:
        return i + 1
    matrix = create_f1_matrix(f, n)
    write_in_file(matrix, folder + '/add_one/', f'add_one_{n}.truth')


def create_f2s():
    funcs = [
        create_mul, create_sum, create_div, create_mod,
        create_min, create_max, create_lcm, create_equal,
        create_gcd, create_abs_sub,
    ]
    for f in funcs:
        for n in range(3, 9):
            f(n, n)


def create_f1s():
    funcs = [
        create_sqr, create_sqrt, create_cbrt, create_add_one,
        create_log, create_log2, create_log10,
    ]

    for f in funcs:
        for n in range(6, 17):
            f(n)


create_f1s()
create_f2s()
