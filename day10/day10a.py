def check_cycle(cycle, X):
    if cycle % 40 == 20:
        return cycle*X
    return 0
with open("input.txt", "rb") as file:
    X = 1
    cycle = 1
    signal_strength_sum = 0
    for line in file:
        line = line.decode("utf-8")[:-1]
        res = line.split(' ')
        cmd = res[0]
        
        if cmd == 'noop':
            cycle += 1
            signal_strength_sum += check_cycle(cycle, X)
        elif cmd == 'addx':
            cycle += 1
            signal_strength_sum += check_cycle(cycle, X)
            cycle += 1
            X += int(res[1])
            signal_strength_sum += check_cycle(cycle, X)
    print(signal_strength_sum)