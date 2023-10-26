with open("input.txt", "rb") as file:
    found_digits = False
    rows = []
    stacks = []
    for line in file:
        line = line.decode("utf-8")
        if not found_digits:
            if any([c.isdigit() for c in line]):
                found_digits = True
                num_cols = max(map(int, filter(lambda c: c.isdigit(), line.split(' '))))
                stacks = [[] for i in range(num_cols)]
                for row in rows[::-1]:
                    for i in range(num_cols):
                        if row[i] != ' ':
                            stacks[i].append(row[i])
                file.readline()
                    
            else:
                rows.append([line[i+1] for i in range(0, len(line), 4)])
        else:
            tokens = line[:-1].split(' ')
            num_to_move, src, dst = int(tokens[1]), int(tokens[3])-1, int(tokens[5])-1
            move = []
            for i in range(num_to_move):
                if len(stacks[src]) == 0:
                    break
                move.append(stacks[src].pop())
            #for i in range(len(move)-1, -1, -1):
            for i in range(len(move)):
                stacks[dst].append(move[i])
            #print(f"Move {num_to_move} from {src} to {dst}")
    final = [stack[-1] for stack in stacks]
    final_str = ""
    for i in range(len(final)):
        final_str += final[i]
    print(final_str)