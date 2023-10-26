from copy import copy
import pprint
with open("input.txt", "rb") as file:
    grid = []
    for line in file:
        line = line[:-1].decode("utf-8")
        grid.append(list(map(int, list(line))))

class VisibilityGrid:

    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.visibility_left = []
        self.visibility_right = []
        self.visibility_up = []
        self.visibility_down = []
        self.calculate_visibility()

    def calculate_visibility(self):
        for i in range(self.height):
            self.visibility_left.append([])
            view = {k: 0 for k in range(10)}
            self.visibility_left[i].append(copy(view))
            for j in range(1, self.width):
                for k in range(10):
                    view[k] += 1
                for k in range(self.grid[i][j-1]+1):
                    view[k] = 1
                self.visibility_left[i].append(copy(view))
            self.visibility_right.append([])
            view = {k: 0 for k in range(10)}
            self.visibility_right[i].append(copy(view))
            for j in range(self.width-2, -1, -1):
                for k in range(10):
                    view[k] += 1
                for k in range(self.grid[i][j+1]+1):
                    view[k] = 1
                self.visibility_right[i].append(copy(view))
            self.visibility_right[i] = self.visibility_right[i][::-1]
        for i in range(self.height):
            self.visibility_up.append([None]*self.width)
            self.visibility_down.append([None]*self.width)
        for j in range(self.width):
            view = {k: 0 for k in range(10)}
            self.visibility_up[0][j] = copy(view)
            for i in range(1, self.height):
                for k in range(10):
                    view[k] += 1
                for k in range(self.grid[i-1][j]+1):
                    view[k] = 1
                self.visibility_up[i][j] = copy(view)
            view = {k: 0 for k in range(10)}
            self.visibility_down[self.height-1][j] = copy(view)
            for i in range(self.height-2, -1, -1):
                for k in range(10):
                    view[k] += 1
                for k in range(self.grid[i+1][j]+1):
                    view[k] = 1
                self.visibility_down[i][j] = copy(view)

        visibilities = []
        for i in range(self.height):
            visibilities.append([])
            for j in range(self.width):
                visibilities[i].append(self.visibility_left[i][j][self.grid[i][j]])
        #pprint.pprint(visibilities)
        visibilities = []
        for i in range(self.height):
            visibilities.append([])
            for j in range(self.width):
                visibilities[i].append(self.visibility_right[i][j][self.grid[i][j]])
        #pprint.pprint(visibilities)
        visibilities = []
        for i in range(self.height):
            visibilities.append([])
            for j in range(self.width):
                visibilities[i].append(self.visibility_up[i][j][self.grid[i][j]])
        #pprint.pprint(visibilities)
        visibilities = []
        for i in range(self.height):
            visibilities.append([])
            for j in range(self.width):
                visibilities[i].append(self.visibility_down[i][j][self.grid[i][j]])
        #pprint.pprint(visibilities)

    def calculate_scenic_score(self):
        scores = []
        for i in range(self.height):
            scores.append([])
            for j in range(self.width):
                height = self.grid[i][j]
                scores[i].append(self.visibility_left[i][j][height] * self.visibility_right[i][j][height] * self.visibility_up[i][j][height] * self.visibility_down[i][j][height])
        #print(scores)
        return scores

            
            

            
visibilty = VisibilityGrid(grid)
print(max(list(map(max, visibilty.calculate_scenic_score()))))
