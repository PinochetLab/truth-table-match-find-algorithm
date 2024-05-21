# -*- coding: utf-8 -*-

import math
import os
import random
import sys
import json
from itertools import product, permutations


def transform(i, n):
    b = bin(2**n - 1 - i)[2:]
    return int(('0'*(n - len(b)) + b)[::-1], 2)


def mb(i, n):
    b = bin(i)[2:]
    return '0'*(n - len(b)) + b


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


def count(row):
    n = int(math.log2(len(row)))
    ans = []
    for k in range(n):
        cs = [[0, 0], [0, 0]]
        for i in range(2**n):
            ri = transform(i, n)
            one = (ri >> (n - 1 - k)) & 1
            cs[one][int(row[i])] += 1
        ans.append(cs[0] + cs[1])
    return ans


def try_find(s1, s2, r1, r2, perm, neg, mask):
    global final_negation
    for final_neg in (0, 1):
        if mask[0]:
            for g in _try_find(s1, s2, r1, r2, final_neg, neg, perm, mask):
                final_negation = final_neg
                yield g
        else:
            for n in (0, 1):
                neg[0] = n
                for g in _try_find(s1, s2, r1, r2, final_neg, neg, perm, mask):
                    final_negation = final_neg
                    yield g


def swap(lst, i, j):
    lst[i], lst[j] = lst[j], lst[i]


def _check(row1, row2, n, final_neg, negations, permutation):
    index = 0
    for x in list(product((1, 0), repeat=n)):
        x = x[::-1]
        old_x = [x[permutation[i]] ^ negations[i] for i in range(n)]
        ind = int(''.join([str(k ^ 1) for k in old_x[::-1]]), 2)
        if int(row2[ind]) ^ final_neg != int(row1[index]):
            return False
        index += 1
    return True


def _try_find(s1, s2, r1, r2, final_neg, negations, permutation, mask, depth=0):
    #print(depth, final_neg, negations, permutation, mask)
    if depth >= len(s1):
        if _check(r1, r2, len(s1), final_neg, negations, permutation):
            yield
        return
    if mask[depth]:
        if depth + 1 < len(s2) and not mask[depth + 1]:
            for neg in (0, 1):
                negations[depth + 1] = neg
                yield from _try_find(s1, s2, r1, r2, final_neg, negations, permutation, mask, depth + 1)
        else:
            yield from _try_find(s1, s2, r1, r2, final_neg, negations, permutation, mask, depth + 1)
        return
    x1, x2, x3, x4 = s2[depth]
    if final_neg:
        x1, x2 = x2, x1
        x3, x4 = x4, x3
    if negations[depth]:
        x1, x3 = x3, x1
        x2, x4 = x4, x2
    t = [x1, x2, x3, x4]
    indices = [i for i in range(depth, len(s1)) if s1[permutation[i]] == t and not mask[i]]
    for ind in indices:
        swap(permutation, depth, ind)
        if depth + 1 < len(s2) and not mask[depth + 1]:
            for neg in (0, 1):
                negations[depth + 1] = neg
                yield from _try_find(s1, s2, r1, r2, final_neg, negations, permutation, mask, depth + 1)
        else:
            yield from _try_find(s1, s2, r1, r2, final_neg, negations, permutation, mask, depth + 1)
        swap(permutation, depth, ind)


def _mask(permutation, used):
    indices = []
    index = 0
    for i in range(len(permutation)):
        while used[index] == '0':
            index += 1
        indices.append(index)
        index += 1
    answer = []
    for i in range(len(permutation)):
        answer.append(indices[permutation[i]])
    return answer


def print_substitution(substitution):
    print('[', end='')
    keys = sorted(substitution.keys())
    for i in range(len(keys)):
        k = keys[i]
        number, neg = substitution[k]
        print(f'{k}={"!" if neg else ""}{number}', end='')
        if i < len(keys) - 1:
            print(', ', end='')
    print('] ', end='')


def process_substitution(substitution):
    return {int(k): tuple(substitution[k]) for k in substitution}


def print_outputs(outs):
    print('[', end='')
    index = 0
    for s, i, n in outs:
        minus = '!' if n else ''
        if s == 'in':
            print(f'{minus}x{i}', end='')
        else:
            print(f'{minus}{i}', end='')
        if index < len(outs) - 1:
            print(', ', end='')
        index += 1
    print(']')


def to_list(outs):
    lst = []
    for k in sorted(outs.keys()):
        lst.append(tuple(outs[k]))
    return lst


def to_index_map(used):
    n = len(used)
    result = {}
    idx = 0
    for i in range(n):
        if used[i] == '1':
            result[i] = idx
            idx += 1
    return result


def next_substitution(row, n, used, i, substitution):
    global lst

    #print(lst)
    index_map1 = to_index_map(used)
    one_c = row.count('1')
    for ic, out, r, oc, c, us in lst:
        if n != ic:
            continue
        if one_c != oc and one_c + oc != 2 ** ic:
            continue
        co = count(row)
        mask = [0] * n
        neg = [0] * n
        perm = list(range(n))
        index_map2 = to_index_map(us)
        conflict = False
        for idx in substitution:
            idx2, negation = substitution[idx]
            if idx not in index_map1 and idx2 not in index_map2:
                continue
            elif (idx in index_map1) != (idx2 in index_map2):
                conflict = True
                break
            mask[index_map1[idx]] = 1
            neg[index_map1[idx]] = negation
            index1 = index_map1[idx]
            index2 = perm.index(index_map2[idx2])
            swap(perm, index1, index2)
        if conflict:
            continue
        for _ in try_find(c, co, r, row, perm, neg, mask):
            real_vars = _mask(list(range(n)), used)
            real_perm = _mask(perm, us)
            substitution = dict()
            outs = {i: ('out', out, final_negation)}
            for idx in range(ic):
                key = real_vars[idx]
                value = (real_perm[idx], neg[idx])
                substitution[key] = value
            pair = (substitution, outs)
            yield pair


final_negation = 0


def next_substitution_with_save(row, n, used, i, saved):
    if i not in saved:
        lst = []
        for elem in next_substitution(row, n, used, i, {}):
            yield elem
            lst.append(elem)
        saved[i] = lst
    else:
        lst = saved[i]
        for elem in lst:
            yield elem


def combine(s1, o1, s2, o2):
    for k in s2:
        if k in s1 and s1[k] != s2[k]:
            return False
    s2.update(s1)
    o2.update(o1)
    return True


def _dfs(saved, substitution, outputs):
    global lines, lst
    indices = list(range(len(lines)))
    random.shuffle(indices)
    yield from dfs(0, saved, substitution, outputs, indices)


def dfs(out_idx, saved, substitution, outputs, indices):
    #print(f'start dfs({out_idx}) {substitution} {outputs}')
    global lines, lst
    #print('lst', lst)
    if out_idx >= len(lines):
        yield substitution, outputs
        return
    split = lines[indices[out_idx]].split()
    used = split[0]
    row = split[1]
    n = int(math.log2(len(row)))
    if n == 1:
        s = {}
        o = {indices[out_idx]: ('in', used.find("1"), 1 - int(row[0]))}
        s.update(substitution)
        o.update(outputs)
        yield from dfs(out_idx + 1, saved, s, o, indices)
        return
    for c_s, c_o in next_substitution(row, n, used, indices[out_idx], substitution):
        c_s.update(substitution)
        c_o.update(outputs)
        yield from dfs(out_idx + 1, saved, c_s, c_o, indices)


if __name__ == "__main__":
    folder1 = 'files3'
    folder2 = 'files'
    use_dfs = True
    outputs = dict()
    #ex = ['ex12.truth', 'ex21.truth', 'ex26.truth']
    ex = sys.argv[1:]
    #files = sys.argv[1:]

    data_name = 'data.txt'

    if os.path.exists(data_name):
        with open(data_name) as rf:
            outputs = json.load(rf)
    else:
        for (_, _, filenames) in os.walk(folder1):
            for filename in filenames:
                with open(f'{folder1}/{filename}') as f:
                    print(filename)
                    lines = [line.rstrip() for line in f]
                    outs = []
                    for i in range(len(lines)):
                        split = lines[i].split()
                        used = split[0]
                        row = split[1]
                        vc = used.count('1')
                        if vc <= 1:
                            continue
                        input_count = int(math.log2(len(row)))
                        one_c = row.count('1')
                        outs.append((input_count, i, row, one_c, count(row), used))
                        outputs[filename] = outs
        with open(data_name, 'w') as wf:
            json.dump(outputs, wf)

    for (_, _, filenames) in os.walk(folder2):
        for filename in filenames:
            with open(f'{folder2}/{filename}') as f:
                #if filename not in ex:
                #    continue
                print(f'process {filename}')
                lines = [line.rstrip() for line in f]
                for fn in outputs:
                    lst = outputs[fn]
                    if use_dfs:
                        saved = {}
                        found = False
                        for s, o in _dfs(saved, {}, {}):
                            print(f'{filename} from {fn}')
                            print(process_substitution(s))
                            print(to_list({int(k): o[k] for k in o}))
                            with open('results.txt', 'a') as wf:
                                wf.write(f'{filename} from {fn}\n')
                                wf.write(str(process_substitution(s)) + '\n')
                                wf.write(str(to_list({int(k): o[k] for k in o})) + '\n')
                            print_substitution(process_substitution(s))
                            print_outputs(to_list(o))
                            found = True
                            break
                        if found:
                            continue
                    else:
                        outs = dict()
                        substitutions_set = {json.dumps((dict(), dict()))}
                        for i in range(len(lines)):
                            split = lines[i].split()
                            used = split[0]
                            row = split[1]
                            vc = used.count('1')
                            input_count = int(math.log2(len(row)))
                            if input_count == 1:
                                outs[i] = ('in', used.find("1"), 1 - int(row[0]))
                                continue
                            one_c = row.count('1')
                            current_substitutions = set()
                            for ic, out, r, oc, c, us in lst:
                                if input_count != ic:
                                    continue
                                if one_c != oc and one_c + oc != 2**ic:
                                    continue
                                co = count(row)
                                final_negation = 0
                                neg = [0]*ic
                                perm = list(range(ic))
                                for _ in try_find(c, co, r, row, perm, neg, [0]*ic):
                                    real_vars = _mask(list(range(input_count)), used)
                                    real_perm = _mask(perm, us)
                                    substitution = dict()
                                    for idx in range(ic):
                                        key = real_vars[idx]
                                        value = (real_perm[idx], neg[idx])
                                        substitution[key] = value
                                    current_substitutions.add(json.dumps((substitution, {i: ('out', out, final_negation)})))
                                    print(f'{folder2}/{filename}({i}) from {folder1}/{fn}({out}) with {substitution}')
                            if len(current_substitutions) > 0:
                                new_set = set()
                                for s1_s in substitutions_set:
                                    s1, o1 = json.loads(s1_s)
                                    for s2_s in current_substitutions:
                                        s2, o2 = json.loads(s2_s)
                                        conflict = False
                                        for k in s2:
                                            if k in s1 and s1[k] != s2[k]:
                                                conflict = True
                                                break
                                        if not conflict:
                                            s2.update(s1)
                                            o2.update(o1)
                                            new_set.add(json.dumps((s2, o2)))
                                substitutions_set = new_set
                                if len(substitutions_set) == 0:
                                    break
                            else:
                                substitutions_set = set()
                                break
                        if len(substitutions_set) > 0:
                            new_s = set()
                            for s1_s in substitutions_set:
                                s1, o1 = json.loads(s1_s)
                                o1.update(outs)
                                new_s.add(json.dumps((s1, o1)))
                            substitutions_set = new_s
                            s, o = json.loads(list(substitutions_set)[0])
                            print(f'{filename} from {fn}')
                            print(process_substitution(s))
                            print(to_list({int(k): o[k] for k in o}))
                            print_substitution(process_substitution(s))
                            print_outputs(to_list({int(k): o[k] for k in o}))
                            break
