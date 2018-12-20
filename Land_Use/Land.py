import numpy as np
import sys


class Area:
    """
    A generic area, consisting of a length and width, 1 unit of length = 1 unit of
    width = 15 meters. This will form the basis of the CropField class. It takes a two-dimensional array
    as an input and converts it into a numpy array, then checks that it is a true 2D array (a list of lists,
    with all sublists being the same length)
    >>> a = [[1, 1, 1, 1], [1, 1, 1], [1, 1, 1, 1], [4, 4, 4, 4]]
    >>> a1 = Area(a)  #doctest: +NORMALIZE_WHITESPACE
    Subarrays must be the same length
    Process finished with exit code 42
    >>> a = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [4, 4, 4, 4]]
    >>> a1 = Area(a)
    >>> print(a1)
    60 m x 60 m area

    >>> a1
    Area('60 m x 60 m')


    """

    def __init__(self, array):
        # convert input array to numpy array
        self.array = np.array(array)
        self.shape = self.array.shape
        self.row_len = self.shape[0]
        # checks that it is a 2D array and not a simple list
        assert type(self.array[0]) is not int, "Area must be a 2-dimensional list, e.g., [[1,1],[1,1]]."
        # this checks that every sublist is the same length. Numpy's shape returns a tuple with the second element
        # empty if the sublists have different lengths. So this simply gives a more meaningful error
        try:
            self.col_len = self.shape[1]
        except (ValueError, IndexError):
            print("Subarrays must be the same length")
            sys.exit(42)
        ix_food = np.isin(self.array, [2, 4])
        self.food_indices = []
        if True in ix_food:
            self.food_indices = list(zip(np.where(ix_food)[0], np.where(ix_food)[1]))
        ix_shelter = np.isin(self.array, [3, 4])
        self.shelter_indices = []
        if True in ix_shelter:
            self.shelter_indices = list(zip(np.where(ix_shelter)[0], np.where(ix_shelter)[1]))
        # This dosen't do anything at the moment, just thinking ahead
        self.developed_indices = []

    def __str__(self) -> str:
        """
        Prints the dimensions of the area. Each extra row and column adds 15 meetrs to the dimensions
        :return: string for printing
        """
        return '{} m x {} m area'.format(
            self.row_len * 15, self.col_len * 15)

    def __repr__(self):
        """
        Basically the same as above, but adds the "Area" class designation
        :return: string for printing
        """
        return "Area('{} m x {} m')".format(
            self.row_len * 15, self.col_len * 15)

    def concatenate(self, area2):
        new_array = np.concatenate((self.array, area2))
        return Area(new_array)

