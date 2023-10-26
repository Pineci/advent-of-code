def print_board(knots, square_size=5):
    board = [['.' for _ in range(square_size)] for _ in range(square_size)]
    #board[square_size-1-tail[1]][tail[0]] = 'T'
    #board[square_size-1-head[1]][head[0]] = 'H'
    for idx, knot in zip(list(range(len(knots)))[::-1], knots[::-1]):
        char = 'H' if idx == 0 else str(idx)
        board[square_size-1-knot[1]][knot[0]] = char
    for line in board:
        print(' '.join(line))
    print(' '.join(["="*square_size*2]))

def update(new_head, tail):
    difference = (new_head[0]-tail[0], new_head[1]-tail[1])
    if abs(difference[0]) <= 1 and abs(difference[1]) <= 1:
        return new_head, tail
    else:
        if difference[0] == -2:
            if difference[1] == 2:
                move = (1, -1)
            elif difference[1] == -2:
                move = (1, 1)
            else:
                move = (1, 0)
        elif difference[0] == 2:
            if difference[1] == 2:
                move = (-1, -1)
            elif difference[1] == -2:
                move = (-1, 1)
            else:
                move = (-1, 0)
        elif difference[1] == -2:
            if difference[0] == 2:
                move = (-1, 1)
            elif difference[0] == -2:
                move = (1, 1)
            else:
                move = (0, 1)
        elif difference[1] == 2:
            if difference[0] == 2:
                move = (-1, -1)
            elif difference[0] == -2:
                move = (1, -1)
            else:
                move = (0, -1)
        new_tail = (new_head[0]+move[0], new_head[1]+move[1])
        return new_head, new_tail

def move(head, direction):
    if direction == 'U':
        move = (0, 1)
    elif direction == 'D':
        move = (0, -1)
    elif direction == 'R':
        move = (1, 0)
    elif direction == 'L':
        move = (-1, 0)
    return (head[0]+move[0], head[1]+move[1])
    

with open("input.txt", "rb") as file:
    knots = [(0, 0) for _ in range(10)]
    visited = {(0, 0)}
    for line in file:
        line = line.decode("utf-8")[:-1]
        direction, amount = line.split(" ")
        amount = int(amount)
        for _ in range(amount):
            knots[0] = move(knots[0], direction)
            for i in range(9):
                knots[i], knots[i+1] = update(knots[i], knots[i+1])
            visited.add(knots[-1])
            #print_board(knots, square_size=6)
print(len(visited))