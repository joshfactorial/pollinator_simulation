from Land_Use.Developed.farm import *
from Animal.Danaus.plexippus import *
import matplotlib.pyplot as plt
import numpy as np


def graphic_display(field: Area = None, moves: np.array = None):
    """
    This will take a field and an array defining the path the pollinator took and turn it into a heatmap
    :param field: an area the pollinator lives on which it spent it's simulated time on
    :param moves: a collection of moves made by the pollinator.
    :return: No return, it simply displays a plot.
    TODO: everything
    """
    if field is None:
        field = StandardTest(1)
    if moves is None:
        b1 = Monarch(field)
        b1.move_one_day()
        moves = b1.moves
    # counts = np.zeros((len(field.array), len(field.array[0])), dtype=int)
    xmoves = []
    ymoves = []
    for move in moves:
        xmoves.append(move[0])
        ymoves.append(move[1])
    heatmap, xedges, yedges = np.histogram2d(xmoves, ymoves, bins=50)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.show()
