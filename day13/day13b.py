from functools import cmp_to_key


def eval_pair(first, second):
    if isinstance(first, list) and isinstance(second, list):
        i = 0
        while True:
            if i == len(first) or i == len(second):
                if len(first) == len(second):
                    return None
                if i == len(first):
                    return True
                if i == len(second):
                    return False
            cmp = eval_pair(first[i], second[i])
            if cmp is not None:
                return cmp
            i += 1
    elif isinstance(first, int) and isinstance(second, int):
        if first < second:
            return True
        if second < first:
            return False
        return None
    elif isinstance(first, int):
        return eval_pair([first], second)
    else:
        return eval_pair(first, [second])

def sorting_func(x, y):
    res = eval_pair(x, y)
    if eval_pair is None:
        return 0
    else:
        return -1 if res else 1
        

with open("input.txt", "rb") as file:
    first, second = [[2]], [[6]]
    packets = [first, second]
    for line in file:
        line = line.decode("utf-8")[:-1]
        if line != '':
            packets.append(eval(line))
    packets = list(sorted(packets, key=cmp_to_key(sorting_func)))
    first_idx, second_idx = packets.index(first), packets.index(second)
    print((first_idx+1)*(second_idx+1))