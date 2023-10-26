from typing import Dict, List, Union, Tuple
from enum import Enum
from queue import PriorityQueue
from copy import copy
import random
import math


class MoveType(Enum):
    TUNNEL = 0
    OPEN = 1

class Path:

    def __init__(self, minutes: int = 30, start: str = 'AA'):
        self.minutes = minutes
        self.start = start
        self.id = random.random()
        self.move_type = []
        self.move_vertex = []
        self.move_cost = []
        self.opened = set()
        self.total_cost = 0

    def set_move(self, type: MoveType, vertex: str, minute_cost: int) -> None:
        self.move_type.append(type)
        self.move_vertex.append(vertex)
        self.move_cost.append(minute_cost)
        self.total_cost = self.total_cost + minute_cost
        if type == MoveType.OPEN:
            self.opened.add(vertex)

    def set_move_tuple(self, type_vertex_cost: Tuple[MoveType, str]) -> None:
        self.set_move(type_vertex_cost[0], type_vertex_cost[1], type_vertex_cost[2])

    def is_open(self, vertex: str) -> bool:
        return vertex in self.opened

    def get_current_vertex(self) -> str:
        for i in range(len(self.move_type)-1, -1, -1):
            if self.move_type[i] == MoveType.TUNNEL:
                return self.move_vertex[i]
        return self.start

    def path_cost(self) -> int:
        return self.total_cost

    def path_reward(self, g: 'Graph'):
        acc = 0
        time_taken = 0
        for idx, move in enumerate(self.move_type):
            time_taken += self.move_cost[idx]
            if move == MoveType.OPEN:
                flow_rate = g.get_flow_rate(self.move_vertex[idx])
                time_remaining = self.minutes - time_taken
                acc += flow_rate * time_remaining
        return acc

    def path_bound(self, g: 'Graph'):
        # Simple bound by checking max if we open all remaining valves in the next step after taking account time to get there
        acc = 0
        current = self.get_current_vertex()
        current_time = self.path_cost()
        for v in g.get_vertices():
            if not self.is_open(v):
                acc += g.get_flow_rate(v) * (self.minutes - min(self.minutes, (current_time + g.get_distance(current, v) + 1)))
        total = acc+self.path_reward(g)
        return total

    def copy(self) -> 'Path':
        new = Path(minutes=self.minutes, start=self.start)
        new.move_type = copy(self.move_type)
        new.move_vertex = copy(self.move_vertex)
        new.move_cost = copy(self.move_cost)
        new.opened = copy(self.opened)
        new.total_cost = self.total_cost
        return new

    def __lt__(self, other):
        return self.id < other.id
    def __le__(self, other):
        return self.id <= other.id
    def __eq__(self, other):
        return self.id == other.id
    def __ne__(self, other):
        return self.id != other.id
    def __gt__(self, other):
        return self.id > other.id
    def __ge__(self, other):
        return self.id >= other.id

    def __str__(self):
        string = ""
        for move_type, move_vertex in zip(self.move_type, self.move_vertex):
            if move_type == MoveType.OPEN:
                string += f"Opening Valve {move_vertex}\n"
            else:
                string += f"Moving to Valve {move_vertex}\n"
        return string[:-1]
        

class Vertex:

    def __init__(self, id: str, flow_rate: int):
        self.id = id
        self.flow_rate = flow_rate

class Graph:

    def __init__(self):
        self.edges: Dict[str, List[str]] = {}
        self.vertices: Dict[str, Vertex] = {}

    def add_vertex(self, v: Vertex):
        self.vertices[v.id] = v
        self.edges[v.id] = []

    def add_edge(self, u_id: str, v_id: str, weight: int = 1):
        self.edges[u_id].append((v_id, weight))

    def get_edges(self, u_id: str):
        return self.edges[u_id]

    def get_flow_rate(self, u_id: str):
        return self.vertices[u_id].flow_rate

    def get_vertices(self) -> List[str]:
        return list(self.vertices.keys())

    def path_valid_next_move(self, path: Path, prioritize_opening=False, prevent_visited=False):
        u = path.get_current_vertex()
        valid_moves = [(MoveType.TUNNEL, v[0], v[1]) for v in list(filter(lambda e: not path.is_open(e[0]), self.get_edges(u)))]
        if self.get_flow_rate(u) > 0:
            if not path.is_open(u):
                if prioritize_opening:
                    valid_moves = [(MoveType.OPEN, u, 1)]
                else:
                    valid_moves.append((MoveType.OPEN, u, 1))
        return valid_moves

    def greedy_path(self, start: str = 'AA', minutes: int = 30) -> Path:
        path = Path(minutes=minutes, start=start)
        for i in range(minutes):
            move = random.choice(self.path_valid_next_move(path, prioritize_opening=True))
            path.set_move_tuple(move)
        return path

    def floyd_warshall(self):
        distances = {src: {dst: math.inf for dst in self.get_vertices()} for src in self.get_vertices()}
        for u in self.get_vertices():
            for edge in self.get_edges(u):
                v, weight = edge
                distances[u][v] = weight
            distances[u][u] = 0
        for k in self.get_vertices():
            for i in self.get_vertices():
                for j in self.get_vertices():
                    potential_shorter = distances[i][k] + distances[k][j]
                    if distances[i][j] > potential_shorter:
                        distances[i][j] = potential_shorter
        return distances

    def calculate_distances(self):
        self.distances = self.floyd_warshall()

    def get_distance(self, u, v) -> int:
        return self.distances[u][v]

    def shrink_graph(self, start: str = 'AA') -> 'Graph':
        vertices_to_keep = []
        for v in self.get_vertices():
            if self.get_flow_rate(v) > 0:
                vertices_to_keep.append(v)
        distances = self.floyd_warshall()
        complete_graph = Graph()
        complete_graph.add_vertex(Vertex(start, self.get_flow_rate(start)))
        for v in vertices_to_keep:
            complete_graph.add_vertex(Vertex(v, self.get_flow_rate(v)))
            complete_graph.add_edge(start, v, distances[start][v])
        for u in vertices_to_keep:
            for v in vertices_to_keep:
                if u != v:
                    complete_graph.add_edge(u, v, distances[u][v])
        return complete_graph


    def best_first_branch_and_bound(self, start: str = 'AA', minutes: int = 30, 
                                    prioritize_opening: bool=True, prevent_visited: bool=True) -> Path:
        queue = PriorityQueue()
        path = Path(start=start, minutes=minutes)
        queue.put((-1*path.path_bound(self), Path(start=start, minutes=minutes)))
        best_path, best_reward = None, None
        count = 0
        while not queue.empty():
            count += 1
            
            bound, path = queue.get(block=False)
            if count % 1000 == 0:
                print(f"Iteration: {count} Queue Size: {queue.qsize()} Path Length: {len(path.move_type)} Path Cost: {path.path_cost()} Reward: {best_reward}")
            bound = bound * -1
            path_reward = path.path_reward(self)
            if best_reward is None or path_reward > best_reward:
                best_path = path
                best_reward = path_reward
            possible_moves = self.path_valid_next_move(path, prioritize_opening=prioritize_opening, prevent_visited=prevent_visited)
            new_paths = [path.copy() for _ in range(len(possible_moves))]
            for p, move in zip(new_paths, possible_moves):
                p.set_move_tuple(move)
            for path in new_paths:
                path_bound = path.path_bound(self)
                if path_bound > best_reward:
                    queue.put((-1*path_bound, path))
        print(best_path)
        return best_reward

with open("input.txt", "rb") as file:
    g = Graph()
    for line in file:
        line = line.decode("utf-8")[:-1].split("; ")
        id, flow_rate = line[0][6:8], int(line[0].split("=")[-1])
        g.add_vertex(Vertex(id, flow_rate))
        target_ids = []
        if "," in line[1]:
            target_ids = line[1].split("valves ")[-1].split(", ")
        else:
            target_ids = [line[1][-2:]]
        for target in target_ids:
            g.add_edge(id, target)
    g_shrunk = g.shrink_graph()
    g_shrunk.calculate_distances()
    best_pressure = g_shrunk.best_first_branch_and_bound()
    print(best_pressure)