import os

with open("input.txt", "rb") as file:
    current = 0
    calories = []
    for line in file:
        if len(line) == 1:
            calories.append(current)
            current = 0
        else:
            current += int(line)
    calories.append(current)
    print(sum(sorted(calories, reverse=True)[:3]))