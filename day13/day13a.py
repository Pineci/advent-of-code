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

with open("input.txt", "rb") as file:
    pairs = []
    first = None
    for line in file:
        line = line.decode("utf-8")[:-1]
        if first is None:
            first = eval(line)
        elif line == '':
            first = None
        else:
            pairs.append((first, eval(line)))
    sum_indices = 0
    for idx, pair in enumerate(pairs):
        first, second = pair
        if eval_pair(first, second):
            sum_indices += idx+1
    print(sum_indices)