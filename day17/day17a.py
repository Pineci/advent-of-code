from enum import Enum
from typing import Tuple
from itertools import repeat

class Pieces(Enum):
    # (x, y) == (0, 0) is the bottom left corner of the piece's bounding box
    horiz = [(0, 0), (1, 0), (2, 0), (3, 0)]
    cross = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
    l = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    vert = [(0, 0), (0, 1), (0, 2), (0, 3)]
    square = [(0, 0), (0, 1), (1, 0), (1, 1)]

class Simulation:

    start_vertical_offset = 4

    def __init__(self, width: int=7):
        self.width = width
        self.solid_pieces = set()
        self.piece = None
        self.max_height = 0
        self.build_floor()
        self.build_walls()

    def build_walls(self):
        for i in range(self.max_height, self.max_height+self.start_vertical_offset+1):
            self.solid_pieces.add((-1, i))
            self.solid_pieces.add((self.width, i))

    def build_floor(self):
        for i in range(self.width):
            self.solid_pieces.add((i, 0))

    def place_piece(self, piece_type: Pieces, bottom_left: Tuple[int, int]):
        piece = piece_type.value
        self.piece = list(map(lambda c: (c[0] + bottom_left[0], c[1] + bottom_left[1]), piece))

    def intersects(self, piece):
        return any(list(map(lambda c: c in self.solid_pieces, piece)))

    def move_down(self):
        temp_piece = list(map(lambda c: (c[0], c[1]-1), self.piece))
        
        if self.intersects(temp_piece):
            for c in self.piece:
                self.solid_pieces.add(c)
                if c[1] > self.max_height:
                    self.max_height = c[1]
                self.build_walls()
            self.piece = None
        else:
            self.piece = temp_piece

    def jet_piece(self, jet):
        dir = 1 if jet == '>' else -1
        temp_piece = list(map(lambda c: (c[0] + dir, c[1]), self.piece))
        if not self.intersects(temp_piece):
            self.piece = temp_piece

    def get_bottom_left_start(self):
        return (2, self.max_height+self.start_vertical_offset)

    def loop(self, num_rocks: int,  jet: str):
        pieces = [Pieces.horiz, Pieces.cross, Pieces.l, Pieces.vert, Pieces.square]
        jet_idx, jet_len = 0, len(jet)
        piece_idx, piece_len = 0, len(pieces)

        for i in range(num_rocks):
            self.place_piece(pieces[piece_idx], bottom_left=self.get_bottom_left_start())
            piece_idx = (piece_idx+1) % piece_len
            #print(self.piece)
            while self.piece is not None:
                self.jet_piece(jet[jet_idx])
                #print(f"{jet[jet_idx]} {self.piece}")
                if jet_idx == 0:
                    print(f"JET RESET ROCK: {i} {i % 5}")
                    self.print(bottom=self.max_height-5)
                jet_idx = (jet_idx+1) % jet_len
                self.move_down()
                #print(f"down {self.piece}")

    def print(self, bottom=0):
        for height in range(self.max_height, bottom, -1):
            line = "|"
            for x in range(self.width):
                point = (x, height)
                if point in self.solid_pieces:
                    line += "#"
                else:
                    line += "."
            line += "|"
            print(line)
        print("+" + "-"*self.width + "+")

with open("input.txt", "rb") as file:
    jet = file.readline().decode('utf-8')[:-1]
print(len(jet))
simulation = Simulation()
simulation.loop(1000000000000, jet)
print(simulation.max_height)
#print(list(filter(lambda c: c[0] >= 0 and c[0] < simulation.width, simulation.solid_pieces)))
#simulation.print()
