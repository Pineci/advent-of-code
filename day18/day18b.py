from disjointset import DisjointSet
from typing import Set, Tuple

def neighbors(coord):
    return [(coord[0]+1, coord[1], coord[2]),
            (coord[0]-1, coord[1], coord[2]),
            (coord[0], coord[1]+1, coord[2]),
            (coord[0], coord[1]-1, coord[2]),
            (coord[0], coord[1], coord[2]+1),
            (coord[0], coord[1], coord[2]-1)]


def process_points(droplets: Set[Tuple[int, int, int]]):
    # Calculate the bounding box of the droplets
    min_point, max_point = None, None
    for coord in droplets:
        if min_point is None:
            min_point = coord
            max_point = coord
        else:
            min_point = (min(min_point[0], coord[0]), min(min_point[1], coord[1]), min(min_point[2], coord[2]))
            max_point = (max(max_point[0], coord[0]), max(max_point[1], coord[1]), max(max_point[2], coord[2]))
    
    # Initialize the universe of possible points
    # Include a +1 border on all sides so the outer component is guarenteed to be connected and enclosing the droplet
    all_points = set()
    for x in range(min_point[0]-1, max_point[0]+2):
        for y in range(min_point[1]-1, max_point[1]+2):
            for z in range(min_point[2]-1, max_point[2]+2):
                all_points.add((x, y, z))

    # Initialize the disjoint set of all points
    components = DisjointSet()
    for point in all_points:
        components.make_set(point)

    # Merge points when they have the same type as their neighbor
    for point in all_points:
        if point in droplets:
            membership = lambda n: n in droplets
        else:
            membership = lambda n: n not in droplets

        for neighbor in neighbors(point):
            if membership(neighbor):
                components.union(point, neighbor)

    # Now, the components data structure has every bubble of the same type in its own connected component
    # Next steps:
    # -- Find the set of the points of the connected component of the enclosing space. Just use the bottom most corner of all points since it
    # is guaranteed to not be in droplets
    # -- Negate this set to find all the points in the enclosed space
    # -- Calculat the bounding surface area of this enclosed space

    enclosing_point = (min_point[0]-1, min_point[1]-1, min_point[2]-1)
    enclosing_root = components.find(enclosing_point)
    enclosing = set()
    enclosed = set()
    for point in all_points:
        if components.find(point) == enclosing_root:
            enclosing.add(point)
        else:
            enclosed.add(point)

    surface_area = 0
    for droplet in enclosed:
        for neighbor in neighbors(droplet):
            if neighbor not in enclosed:
                surface_area += 1
    return surface_area
    
    
droplet_coords = set()
with open("input.txt", "rb") as file:
    for line in file:
        droplet_coords.add(eval("(" + line.decode("utf-8")[:-1] + ")"))
print(process_points(droplet_coords))