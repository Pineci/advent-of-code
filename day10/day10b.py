def check_cycle(cycle, X):
    pos = (cycle-1) % 40
    if abs(pos-X) <= 1:
        result = "#"
    else:
        result = "."
    print(f"Cycle: {cycle} Pos: {pos} X: {X} Result: {result}")
    return result

with open("input.txt", "rb") as file:
    X = 1
    cycle = 1
    chars = []
    for line in file:
        line = line.decode("utf-8")[:-1]
        res = line.split(' ')
        cmd = res[0]
        print(res)
        if cmd == 'noop':
            chars.append(check_cycle(cycle, X))
            cycle += 1
        elif cmd == 'addx':
            chars.append(check_cycle(cycle, X))
            cycle += 1
            chars.append(check_cycle(cycle, X))
            X += int(res[1])
            cycle += 1
        
    for i in range(0, len(chars), 40):
        print(' '.join(chars[i:i+40]))