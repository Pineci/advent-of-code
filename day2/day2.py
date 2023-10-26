import os

def calculate_round(first, second):

    def ret(values):
        match second:
            case 'X':
                return values[0] 
            case 'Y':
                return values[1] + 3
            case 'Z':
                return values[2] + 6

    match first:
        case 'A':
            return ret([3, 1, 2])
        case 'B':
            return ret([1, 2, 3])
        case 'C':
            return ret([2, 3, 1])

with open("input.txt", "rb") as file:
    score = 0
    for line in file:
        line = bytes.decode(line)
        first = line[0]
        second = line[-2]
        print(f"{first}, {second}")
        score += calculate_round(first, second)
    print(score)