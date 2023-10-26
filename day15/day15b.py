class Sensor:

    def __init__(self, sensor_pos, beacon_pos):
        self.sensor_pos = sensor_pos
        self.beacon_pos = beacon_pos
        self.beacon_dist = self.get_beacon_dist()

    def get_beacon_dist(self):
        return abs(self.sensor_pos[0] - self.beacon_pos[0]) + abs(self.beacon_pos[1] - self.sensor_pos[1])

    def dist_remaining(self, target_row):
        return self.beacon_dist - abs(self.sensor_pos[1] - target_row)

    def blocked_positions(self, target_row, size):
        dist_remaining = self.dist_remaining(target_row)
        position_range = []
        if dist_remaining >= 0:
            start, end = self.sensor_pos[0] - dist_remaining, self.sensor_pos[0] + dist_remaining
            start, end = max(0, start), min(size, end)
            position_range = [start, end]
        return position_range

class Board:

    def __init__(self, size, sensors):
        self.size = size
        self.sensors = sensors

    def merge_intervals(self, interval1, interval2):
        if interval1[0] > interval2[0]:
            return self.merge_intervals(interval2, interval1)
        if interval1[1] >= interval2[1]:
            return [interval1]
        elif interval2[0] <= interval1[1]:
            return [[interval1[0], interval2[1]]]
        else:
            return [interval1, interval2]

    def inspect_row(self, row):
        blocked_intervals = list(filter(lambda l: len(l) > 0, [sensor.blocked_positions(row, self.size) for sensor in self.sensors]))
        sorted_intervals = sorted(blocked_intervals, key=lambda i: i[0])
        finished_intervals = []
        current = sorted_intervals[0]
        for i in range(1, len(sorted_intervals)):
            merged = self.merge_intervals(current, sorted_intervals[i])
            current = merged[-1]
            if len(merged) == 2:
                finished_intervals.append(merged[0])
        finished_intervals.append(current)
        return finished_intervals

    def inspect_board(self):
        for row in range(self.size+1):
            if row % 1000 == 0:
                print(row)
            inspection_results = self.inspect_row(row)
            if len(inspection_results) > 1:
                x = inspection_results[0][1] + 1
                return [x, row]
        raise ValueError("Not found!")

    def tuning_frequency(self, position):
        return position[0]*4000000 + position[1]

    def find_tuning_frequency(self):
        return self.tuning_frequency(self.inspect_board())

with open("input.txt", "rb") as file:
    sensors = []
    for line in file:
        sensor, beacon = list(map(lambda x: list(map(int, x.split('x=')[-1].split(", y="))), line.decode("utf-8")[:-1].split(":")))
        sensors.append(Sensor(sensor, beacon))
    board = Board(4000000, sensors)
    print(board.find_tuning_frequency())
    
