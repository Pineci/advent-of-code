from copy import deepcopy
from time import sleep
from typing import Tuple, List
from queue import PriorityQueue


class Terrain:
    
    def __init__(self, height_map):
        self.height_map = height_map
        self.num_cols = len(self.height_map[0])
        self.num_rows = len(self.height_map)
        self.neighbors = {}
        print(f"Initializing terrain with size {(self.num_rows, self.num_cols)}")
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                pos = (i, j)
                self.neighbors[pos] = self.climbable_neighbors(pos)
        print(f"Initialized!")

    def get_height(self, pos: Tuple[int, int]) -> int:
        return self.height_map[pos[0]][pos[1]]

    def valid_point(self, p):
        return p[0] >= 0 and p[0] < self.num_rows and p[1] >= 0 and p[1] < self.num_cols

    def climbable_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        possible_neighbors = list(map(lambda d: (pos[0]+d[0], pos[1]+d[1]), directions))
        valid_neighbors = list(filter(self.valid_point, possible_neighbors))
        climable_neighbors = list(filter(lambda p: self.get_height(pos) - self.get_height(p) >= -1, valid_neighbors))
        return climable_neighbors

    def dfs(self, start, end):
        v_init = {pos: False for pos in self.neighbors.keys()}
        def bfs_internal(current, dist_traveled=0, visited=v_init):
            if current == end:
                return dist_traveled
            visited[current] = True
            explore_neighbors = list(filter(lambda p: not visited[p], self.neighbors[current]))
            for n in explore_neighbors:
                return bfs_internal(n, dist_traveled+1, deepcopy(visited))
        return bfs_internal(start)

    def bfs_distance(self, end):
        visited = {pos: False for pos in self.neighbors.keys()}
        queue = PriorityQueue()
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                pos = (i, j)
                if self.get_height(pos) == 1:
                    queue.put((0, pos))
                    visited[pos] = True
        counter = 0
        while True:
            counter += 1
            dist, current = queue.get(block=False)
            visited[current] = True
            #if counter % 100 == 0:
            #    print(counter)
            if current == end:
                return dist
            #print(f"Evaluating {(dist, current)} Counter: {counter} Neighbors: {self.neighbors[current]}")
            for n in self.neighbors[current]:
                if not visited[n]:
                    #print(f"Putting {(dist+1, n)}, Visited: {visited[n]}")
                    queue.put((dist+1, n))
                    visited[n] = True

with open("input.txt", "rb") as file:
    height_map = []
    start, end = None, None
    for line in file:
        line = [*line.decode("utf-8")[:-1]]
        if 'S' in line:
            start = (len(height_map), line.index('S'))
            line[start[1]] = 'a'
        if 'E' in line:
            end = (len(height_map), line.index('E'))
            line[end[1]] = 'z'
        height_map.append(list(map(lambda c: ord(c)-96, line)))
    terrain = Terrain(height_map)
    print(terrain.bfs_distance(end))