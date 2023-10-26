import os

def char_score(char: str):
    sum = 26 if char.isupper() else 0
    return sum + ord(char)%32

def get_score(line1, line2, line3):
    set1, set2, set3 = set(line1), set(line2), set(line3)
    return char_score(set1.intersection(set2).intersection(set3).pop())

with open("input.txt", "rb") as file:
    lines = []
    for line in file:
        lines.append(line.decode("utf-8")[:-1])

score = 0
for i in range(0, len(lines), 3):
    line1, line2, line3 = lines[i], lines[i+1], lines[i+2]
    score += get_score(line1, line2, line3)
print(f"SCORE {score}")