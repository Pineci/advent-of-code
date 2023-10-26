class Sensor:

    def __init__(self, sensor_pos, beacon_pos):
        self.sensor_pos = sensor_pos
        self.beacon_pos = beacon_pos

    def beacon_dist(self):
        return abs(self.sensor_pos[0] - self.beacon_pos[0]) + abs(self.beacon_pos[1] - self.sensor_pos[1])

    def dist_remaining(self, target_row):
        return self.beacon_dist() - abs(self.sensor_pos[1] - target_row)

    def blocked_positions(self, target_row):
        dist_remaining = self.dist_remaining(target_row)
        positions = set()
        if dist_remaining >= 0:
            start, end = self.sensor_pos[0] - dist_remaining, self.sensor_pos[0] + dist_remaining
            for k in range(start, end+1):
                positions.add(k)
        return positions

    def beacons_in_target_row(self, target_row):
        if self.beacon_pos[1] == target_row:
            return {self.beacon_pos[0]}
        else:
            return set()

with open("input.txt", "rb") as file:
    sensors = []
    for line in file:
        sensor, beacon = list(map(lambda x: list(map(int, x.split('x=')[-1].split(", y="))), line.decode("utf-8")[:-1].split(":")))
        sensors.append(Sensor(sensor, beacon))
    target_row = 2000000
    blocked_positions = set()
    for sensor in sensors:
        blocked_positions = blocked_positions.union(sensor.blocked_positions(target_row))
    for sensor in sensors:
        blocked_positions = blocked_positions.difference(sensor.beacons_in_target_row(target_row))
    print(len(blocked_positions))
    
