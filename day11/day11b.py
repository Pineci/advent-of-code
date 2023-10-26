class Monkey:

    def __init__(self):
        pass

def print_monkeys(monkeys):
    for idx in range(len(monkeys)):
        print(f"Monkey {idx}: {monkeys[idx].items}")
    print()

def eval_round(monkeys, num_rounds):
    inspected = [0] * len(monkeys)
    modulus = 1
    for monkey in monkeys:
        modulus *= monkey.divisor
    for round in range(num_rounds):
        for idx in range(len(monkeys)):
            monkey = monkeys[idx]
            for item in monkey.items:
                inspected[idx] += 1
                new = monkey.operation(item) % modulus
                if monkey.test(new):
                    monkeys[monkey.true_throw_to].items.append(new)
                else:
                    monkeys[monkey.false_throw_to].items.append(new)
            monkey.items = []
    return inspected

with open("input.txt", "rb") as file:
    monkeys = []
    info_index = 0
    monkey = Monkey()
    for line in file:
        line = line.decode("utf-8")[:-1]
        if line == '':
            monkeys.append(monkey)
            info_index = 0
            monkey = Monkey()
        else:
            match info_index:
                case 0:
                    monkey.id = int(line.split(' ')[-1][:-1])
                case 1:
                    monkey.items = list(map(int, line.split(':')[-1].split(',')))
                case 2:
                    op = line.split(' = ')[-1]
                    monkey.operation = lambda old, op=op: eval(op)
                case 3:
                    divisor = int(line.split('by ')[-1])
                    monkey.test = lambda x, div=divisor: x % div == 0
                    monkey.divisor = divisor
                case 4:
                    monkey.true_throw_to = int(line.split('monkey ')[-1])
                case 5:
                    monkey.false_throw_to = int(line.split('monkey ')[-1])
            info_index += 1
    monkeys.append(monkey)
    result = eval_round(monkeys, 10000)
    print(result)
    max_2 = sorted(result, reverse=True)[:2]
    print(max_2[0]*max_2[1])