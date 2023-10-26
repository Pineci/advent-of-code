import os

def interval_contains(first, second):
    return first[0] <= second[0] and first[1] >= second[1]

with open("input.txt", "rb") as file:
    count = 0
    for line in file:
        first, second = line.decode("utf-8")[:-1].split(",")
        first = list(map(int, first.split("-")))
        second = list(map(int, second.split("-")))
        if interval_contains(first, second) or interval_contains(second, first):
            count += 1
print(count)
