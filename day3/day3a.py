import os

def char_score(char: str):
    sum = 26 if char.isupper() else 0
    return sum + ord(char)%32

def get_score(line):
    n = len(line) // 2
    first, second = set(line[:n]), set(line[n:])

    return char_score(first.intersection(second).pop())

with open("input.txt", "rb") as file:
    score = 0
    for line in file:
        score += get_score(line.decode("utf-8"))
    print(score)