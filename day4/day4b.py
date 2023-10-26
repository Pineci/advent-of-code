import os

def interval_disjoint(first, second):
    if second[0] < first[0]:
        return interval_disjoint(second, first)
    return first[1] < second[0]

with open("input.txt", "rb") as file:
    count = 0
    for line in file:
        first, second = line.decode("utf-8")[:-1].split(",")
        first = list(map(int, first.split("-")))
        second = list(map(int, second.split("-")))
        if not interval_disjoint(first, second):
            count += 1
print(count)
