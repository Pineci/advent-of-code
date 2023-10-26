from queue import PriorityQueue
from typing import Optional, Tuple, List
from copy import deepcopy
from math import ceil


class Path:

    def __init__(self, minutes_elapsed, robots, resources):
        self.minutes_elapsed = minutes_elapsed
        self.robots = robots
        self.resources = resources
        self.unit_types = ["ore", "clay", "obsidian", "geode"]

    def copy(self):
        return Path(self.minutes_elapsed, deepcopy(self.robots), deepcopy(self.resources))

    def __lt__(self, other: 'Path'):
        return self.__hash__() < other.__hash__()

    def __str__(self):
        return f"Elapsed: {self.minutes_elapsed} Robots: {self.robots} Resources: {self.resources}"

    def get_priority(self):
        priority = 0
        priority += self.robots["ore"]
        priority += self.robots["clay"]
        priority += self.robots["obsidian"] * 100
        priority += self.robots["geode"] * 10000
        return priority

    def beats(self, other: 'Path'):
        beats = True
        #beats = beats and self.minutes_elapsed <= other.minutes_elapsed
        #for unit in self.unit_types:
            #beats = beats and self.resources[unit] >= other.resources[unit]
            #beats = beats and self.robots[unit] > other.robots[unit]
        beats = beats and self.robots["geode"] >= other.robots["geode"]
        return beats

class Blueprint:

    def __init__(self, num_minutes: int = 24):
        self.id: int = 0
        self.ore_cost: int = None 
        self.clay_cost: int = None
        self.obsidian_cost: Tuple[int, int] = None
        self.geode_cost: Tuple[int, int] = None
        self.unit_types = ["ore", "clay", "obsidian", "geode"]
        self.max_minutes = num_minutes

    def __str__(self):
        return f"Blueprint {self.id} | Ore = {self.ore_cost} | Clay = {self.clay_cost} | Obsidian = {self.obsidian_cost} | Geode: {self.geode_cost}"

    def path_reward(self, path: Path):
        resources = path.resources
        return resources["geode"]

    def path_bound(self, path: Path, debug=False):
        minutes_elapsed, robots, resources = path.minutes_elapsed, path.robots, path.resources
        minutes_remaining = self.max_minutes - minutes_elapsed
        bound = self.path_reward(path) # First count reward we've already achieved
        bound += minutes_remaining * robots["geode"] # Add on production from robots we already have
        minutes_to_geode = self.num_minutes_to_buy_robot("geode", path)
        if minutes_to_geode is None:
            minutes_to_obsidian = self.num_minutes_to_buy_robot("obsidian", path)
            if debug:
                print(f"Minutes to Obsidian: {minutes_to_obsidian}")
            if minutes_to_obsidian is None:
                minutes_to_clay = self.num_minutes_to_buy_robot("clay", path)
                minutes_elapsed = minutes_to_clay
                clay, clay_robots = resources["clay"], robots["clay"]
                while clay < self.obsidian_cost[1]:
                    clay += clay_robots
                    clay_robots += 1
                    minutes_elapsed += 1
                minutes_to_obsidian = minutes_elapsed
            minutes_elapsed = minutes_to_obsidian
            obsidian, obsidian_robots = resources["obsidian"], robots["obsidian"]
            while obsidian < self.geode_cost[1]:
                obsidian += obsidian_robots
                obsidian_robots += 1
                minutes_elapsed += 1
            minutes_to_geode = minutes_elapsed
        
        minutes_remaining_after_buying_more = minutes_remaining - minutes_to_geode
        if debug:
            print(f"Minutes to Geode: {minutes_to_geode}")
            print(f"Minutes Remaining after buying geode: {minutes_remaining_after_buying_more}")
        new_geode_robots = 1
        while minutes_remaining_after_buying_more > 0:
            bound += new_geode_robots
            new_geode_robots += 1
            minutes_remaining_after_buying_more -= 1
        #bound += minutes_remaining * (minutes_remaining-1)/2 # Add on production from robots we build every minute until end
        return bound

    def unit_to_cost(self, unit):
        match unit:
            case "geode":
                return self.geode_cost
            case "ore":
                return self.ore_cost
            case "clay":
                return self.clay_cost
            case "obsidian":
                return self.obsidian_cost

    def num_minutes_to_buy_robot(self, robot: str, path: Path):
        resources = path.resources
        robots = path.robots
        match robot:
            case "ore":
                if resources["ore"] >= self.ore_cost:
                    return 1
                if robots["ore"] == 0:
                    return None
                return 1 + ceil((self.ore_cost - resources["ore"]) / robots["ore"])
            case "clay":
                if resources["ore"] >= self.clay_cost:
                    return 1
                if robots["ore"] == 0:
                    return None
                return 1 + ceil((self.clay_cost - resources["ore"]) / robots["ore"])
            case "obsidian":
                ore_cost, clay_cost = self.obsidian_cost
                if resources["ore"] >= ore_cost and resources["clay"] >= clay_cost:
                    return 1
                if robots["ore"] == 0 or robots["clay"] == 0:
                    return None
                minutes_to_ore = 1 + ceil((ore_cost - resources["ore"]) / robots["ore"])
                minutes_to_clay = 1 + ceil((clay_cost - resources["clay"]) / robots["clay"])
                return max(minutes_to_clay, minutes_to_ore)
            case "geode":
                ore_cost, obsidian_cost = self.geode_cost
                if resources["ore"] >= ore_cost and resources["obsidian"] >= obsidian_cost:
                    return 1
                if robots["ore"] == 0 or robots["obsidian"] == 0:
                    return None
                minutes_to_ore = 1 + ceil((ore_cost - resources["ore"]) / robots["ore"])
                minutes_to_obsidian = 1 + ceil((obsidian_cost - resources["obsidian"]) / robots["obsidian"])
                return max(minutes_to_obsidian, minutes_to_ore)

    def path_allowed_next_move(self, path: Path) -> List[Tuple[str, int]]:
        moves = []
        for unit_type in self.unit_types:
            num_minutes = self.num_minutes_to_buy_robot(unit_type, path)
            if num_minutes is not None and (path.minutes_elapsed + num_minutes) < self.max_minutes:
                moves.append((unit_type, num_minutes))
        return moves[::-1]

    def path_add_move(self, path: Path, move: Optional[Tuple[str, int]] = None):
        #print(f"Path: {path} Move: {move}")
        if move is None:
            num_minutes = self.max_minutes - path.minutes_elapsed
            new_robot_type = None
        else:
            new_robot_type, num_minutes = move
        new_path = path.copy()
        for type in new_path.robots.keys():
            new_path.resources[type] += new_path.robots[type] * num_minutes
        if new_robot_type is not None:
            new_path.robots[new_robot_type] += 1
        match new_robot_type:
            case "ore":
                new_path.resources["ore"] -= self.ore_cost
            case "clay":
                new_path.resources["ore"] -= self.clay_cost
            case "obsidian":
                ore_cost, clay_cost = self.obsidian_cost
                new_path.resources["ore"] -= ore_cost
                new_path.resources["clay"] -= clay_cost
            case "geode":
                ore_cost, obsidian_cost = self.geode_cost
                new_path.resources["ore"] -= ore_cost
                new_path.resources["obsidian"] -= obsidian_cost
            case _:
                pass
        new_path.minutes_elapsed += num_minutes
        #print(f"New Path: {new_path}")
        return new_path


    def solve(self):
        robots = {unit_type: 0 for unit_type in self.unit_types}
        robots["ore"] = 1
        resources = {unit_type: 0 for unit_type in self.unit_types}

        queue = PriorityQueue()
        path = Path(0, robots, resources)
        queue.put((-1*self.path_bound(path), path))
        best_path, best_reward = None, None
        count = 0
        while not queue.empty():
            count += 1
            bound, path = queue.get(block=False)
            #print(f"Count: {count} Path: {path}")
            
            bound = bound * -1
            next_moves = self.path_allowed_next_move(path)
            if len(next_moves) == 0:
                path = self.path_add_move(path)
            if count % 1000 == 0:
                print(f"Iteration: {count} Queue Size: {queue.qsize()} Path: {path} Best Reward: {best_reward} Path Bound: {bound} Next Moves: {next_moves}")
            path_reward = self.path_reward(path)
            if best_reward is None or path_reward > best_reward:
                best_path = path
                best_reward = path_reward
                print(f"New Best Path: {best_path} Best Reward: {best_reward}")
            
            new_paths = [self.path_add_move(path, move) for move in next_moves]
            if count % 1000 == 0:
                for path in new_paths:
                    print(f"New Path: {path} Bound: {self.path_bound(path, debug=True)}")
            #print(f"Original Path: {path}")
            for path in new_paths:
                path_bound = self.path_bound(path)
                if path_bound > best_reward:
                    queue.put((-1*path_bound, path))
            #if count > 5:
            #    break
        return best_reward


with open("test.txt", "rb") as file:
    blueprints = []
    blueprint = Blueprint()
    index = 0
    for line in file:
        blueprint_line = line.decode("utf-8")[:-1].split(":")
        blueprint.id = int(blueprint_line[0].split(" ")[-1])
        costs = list(map(lambda x: x[1:], blueprint_line[1][:-1].split(".")))
        for idx, cost in enumerate(costs):
            tokens = cost.split(" ")[4:]
            if idx == 0:
                blueprint.ore_cost = int(tokens[0])
            elif idx == 1:
                blueprint.clay_cost = int(tokens[0])
            elif idx == 2:
                blueprint.obsidian_cost = (int(tokens[0]), int(tokens[3]))
            elif idx == 3:
                blueprint.geode_cost = (int(tokens[0]), int(tokens[3]))
        blueprints.append(blueprint)
        blueprint = Blueprint()
    #print(blueprints[0])
    #print(f"Best Reward: {blueprints[0].solve()}")
    print(blueprints[1])
    print(f"Best Reward: {blueprints[1].solve()}")
