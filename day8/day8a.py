with open("input.txt", "rb") as file:
    grid = []
    for line in file:
        line = line[:-1].decode("utf-8")
        grid.append(list(map(int, list(line))))

class Visibility:

    def __init__(self):
        self.up, self.down, self.left, self.right = 0, 0, 0, 0

    def is_visible(self, height):
        return height > self.up or height > self.down or height > self.left or height > self.right

    def __repr__(self):
        return f"Left: {self.left} Right: {self.right} Up: {self.up} Down: {self.down}"

width, height = len(grid[0]), len(grid)

# Initialize
visibility = [[Visibility() for _ in range(width)] for _ in range(height)]

# Pass once in each direction
for i in range(1, height-1):
    for j in range(1, width-1):
        visibility[i][j].left = max(visibility[i][j-1].left, grid[i][j-1])
for i in range(1, height-1):
    for j in range(width-2, 0, -1):
        visibility[i][j].right = max(visibility[i][j+1].right, grid[i][j+1])
for j in range(1, width-1):
    for i in range(1, height-1):
        visibility[i][j].up = max(visibility[i-1][j].up, grid[i-1][j])
for j in range(1, width-1):
    for i in range(height-2, 0, -1):
        visibility[i][j].down = max(visibility[i+1][j].down, grid[i+1][j])

# Count visible
num_visible = width*height - (width-2)*(height-2)
for i in range(1, width-1):
    for j in range(1, height-1):
        num_visible += 1 if visibility[i][j].is_visible(grid[i][j]) else 0
print(num_visible)