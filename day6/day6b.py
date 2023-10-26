NUM_CONTINUOUS = 14

with open("input.txt", "rb") as file:
    line = file.readline().decode("utf-8")
    previous = list(line[:NUM_CONTINUOUS])
    for i in range(NUM_CONTINUOUS, len(line)):
        if len(set(previous)) == NUM_CONTINUOUS:
            break
        else:
            previous = previous[1:]
            previous.append(line[i])
    print(i)