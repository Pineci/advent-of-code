class Environment:

    def __init__(self):
        self.rocks = []
        self.rested_sand = []
        self.leftmost, self.rightmost = 500, 500

    def extend_lists(self, length):
        while length > len(self.rocks):
            self.rocks.append(set())
        while length > len(self.rested_sand):
            self.rested_sand.append(set())

    def add_rock(self, pos):
        self.extend_lists(pos[1]+1)
        self.rocks[pos[1]].add(pos[0])
        self.rightmost = max(pos[0], self.rightmost)
        self.leftmost = min(pos[0], self.leftmost)

    def add_rested_sand(self, pos):
        self.extend_lists(pos[1]+1)
        self.rested_sand[pos[1]].add(pos[0])
        self.rightmost = max(pos[0], self.rightmost)
        self.leftmost = min(pos[0], self.leftmost)

    def drop_sand(self):
        current = (500, 0)
        if self.blocked_at(current):
            return False
        while True:
            down = (current[0], current[1]+1)
            if not self.blocked_at(down):
                current = down
                continue
            left = (down[0]-1, down[1])
            if not self.blocked_at(left):
                current = left
                continue
            right = (down[0]+1, down[1])
            if not self.blocked_at(right):
                current = right
                continue
            break
        self.add_rested_sand(current)
        return True

    def simulate(self):
        in_progress = True 
        while in_progress:
            in_progress = self.drop_sand()
    
    def count_sand(self):
        acc = 0
        for sand_row in self.rested_sand:
            acc += len(sand_row)
        return acc

    def blocked_at(self, pos):
        return pos[0] in self.rocks[pos[1]] or  pos[0] in self.rested_sand[pos[1]]

    def get_width(self):
        return self.rightmost-self.leftmost+1

    def get_height(self):
        return len(self.rocks)

    def print_env(self):
        width = self.get_width()
        for rock_row, sand_row in zip(self.rocks, self.rested_sand):
            row = ["."] * width
            for rock in rock_row:
                idx = rock-self.leftmost
                row[idx] = "#"
            for sand in sand_row:
                idx = sand-self.leftmost
                row[idx] = "o"
            print(''.join(row))
        print(''.join(["="]*2*width))

with open("input.txt", "rb") as file:
    rock_lines = []
    for line in file:
        line = line.decode("utf-8")[:-1]
        rock_lines.append(list(map(lambda c: list(map(int, c.split(','))), line.split(' -> '))))
    env = Environment()
    for rock_line in rock_lines:
        for i in range(len(rock_line)-1):
            first, second = rock_line[i], rock_line[i+1]
            first_i, first_j = first
            second_i, second_j = second
            if first_i == second_i:
                start, end = min(first_j, second_j), max(first_j, second_j)
                for k in range(start, end+1):
                    env.add_rock((first_i, k))
            else:
                start, end = min(first_i, second_i), max(first_i, second_i)
                for k in range(start, end+1):
                    env.add_rock((k, second_j))
    width = env.get_width()
    height = env.get_height()
    for k in range(500-height*2, 500+height*2+1):
        env.add_rock((k, height+1))
    env.simulate()
    #env.print_env()
    print(env.count_sand())