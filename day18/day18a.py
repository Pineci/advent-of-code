def neighbors(coord):
    return [(coord[0]+1, coord[1], coord[2]),
            (coord[0]-1, coord[1], coord[2]),
            (coord[0], coord[1]+1, coord[2]),
            (coord[0], coord[1]-1, coord[2]),
            (coord[0], coord[1], coord[2]+1),
            (coord[0], coord[1], coord[2]-1)]

with open("input.txt", "rb") as file:
    droplet_coords = set()
    for line in file:
        droplet_coords.add(eval("(" + line.decode("utf-8")[:-1] + ")"))

surface_area = 0
for droplet in droplet_coords:
    for neighbor in neighbors(droplet):
        if neighbor not in droplet_coords:
            surface_area += 1
print(surface_area)