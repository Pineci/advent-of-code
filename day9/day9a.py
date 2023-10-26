def move(head, tail, direction):
    if direction == 'U':
        move = (0, 1)
    elif direction == 'D':
        move = (0, -1)
    elif direction == 'R':
        move = (1, 0)
    elif direction == 'L':
        move = (-1, 0)
    new_head = (head[0]+move[0], head[1]+move[1])
    difference = (new_head[0]-tail[0], new_head[1]-tail[1])
    if abs(difference[0]) <= 1 and abs(difference[1]) <= 1:
        return new_head, tail
    else:
        return new_head, head

with open("input.txt", "rb") as file:
    head, tail = (0, 0), (0, 0)
    visited = {tail}
    for line in file:
        line = line.decode("utf-8")[:-1]
        direction, amount = line.split(" ")
        amount = int(amount)
        for _ in range(amount):
            head, tail = move(head, tail, direction)
            visited.add(tail)
print(len(visited))