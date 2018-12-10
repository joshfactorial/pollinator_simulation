import numpy as np


class Butterfly:
    def __init__(self):
        self.position = [0, 0]
        array = []
        self.moves = array

    def move(self):
        posn1 = self.position
        self.position = [3, 3]
        posn2 = self.position
        self.moves.append(posn1)
        self.moves.append(posn2)
        self.position = [4, 4]
        posn3 = self.position
        self.moves.append(posn3)


b = Butterfly()
b.move()
print(b.position)
print(b.moves)