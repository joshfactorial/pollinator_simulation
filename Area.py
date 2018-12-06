#!/home/joshua/anaconda3/bin/python

import numpy as np
import sys
import math


class Area:
    """
    A generic area, consisting of a length and width, 1 unit of length = 1 unit of
    width = 15 meters. This will form the basis of the CropField class. It takes a two-dimensional array
    as an input and converts it into a numpy array, then checks that it is a true 2D array (a list of lists,
    with all sublists being the same length)
    >>>Area([[1,1,1],[1,1,1],[2,2,2]])

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
            sys.exit(1)

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


class CropField(Area):
    """
    This is a versioun of the Area class that takes an input array with all elements being equal to 1, 2, or 3.
    Where 1 is a crop, 2 food, and 3 shelter. It can print out a simple graphic interpretation of this array
    (with '=' being crop, 'o' being a food source, and '*' being shelter (trees))
    TODO: Create a better graphical representation
    """

    def __init__(self, array):
        # Initializes the object as an Area class to check that it is truly 2D
        Area.__init__(self, array)
        values = [1, 2, 3, 4]
        if False in np.isin(self.array, values):
            raise ValueError(
                "Values of CropField must be either 1 (crop), 2 (food), 3 (shelter), or 4 (mixed food and shelter)")
        ix_food = np.isin(self.array, [2, 4])
        self.food_indices = []
        if True in ix_food:
            self.food_indices = list(zip(np.where(ix_food)[0], np.where(ix_food)[1]))
        ix_shelter = np.isin(self.array, [3, 4])
        self.shelter_indices = []
        if True in ix_shelter:
            self.shelter_indices = list(zip(np.where(ix_shelter)[0], np.where(ix_shelter)[1]))

    def __to_string(self):
        string_version = ''
        for row in range(self.row_len):
            for column in range(self.col_len):
                if self.array[row][column] == 1:
                    string_version += '='
                elif self.array[row][column] == 2:
                    string_version += 'o'
                elif self.array[row][column] == 3:
                    string_version += '*'
                elif self.array[row][column] == 4:
                    string_version += '@'
                else:
                    print("values must be either 1 (crop), 2 (food), 3 (shelter), or 4 (mixed food/shelter)")
            if row != self.row_len:
                string_version += '\n'
        return string_version

    def __str__(self) -> str:
        return self.__to_string()

    def __repr__(self) -> str:
        return self.__to_string()

    def get_crop_amt(self):
        return (self.array == 1).sum()

    def get_food_amt(self):
        return (self.array == 2).sum()

    def get_shelter_amt(self):
        return (self.array == 3).sum()

    def raw(self):
        string_version = ''
        for row in range(self.row_len):
            for column in range(self.col_len):
                string_version += str(self.array[row][column])
                # if column != self.col_len - 1:
                #     string_version += " "
            if row != self.row_len:
                string_version += '\n'
        print(string_version)

    @classmethod
    def random_field(cls, length: int, width: int, percent_crops: int=100, percent_food: int=0, percent_shelter: int=0):
        """
        Creates a random field given the dimensions. Picks placement of food and shelter randomly

        :param length: Total number of rows in the field
        :param width: Total number of columns in the field
        :param percent_crops: Whole number percent of crops in the field
        :param percent_food: Whole number percent of Pollinator food in the field
        :param percent_shelter: Whole number percent of trees in the field
        :return: CropField | None
        """
        if percent_crops + percent_food + percent_shelter != 100:
            raise ValueError("The percentages do not add up to 100")
        area = length * width
        # find the number of squares for each type of cell
        number_crop_cells = math.ceil(percent_crops / 100 * area)
        number_food_cells = math.ceil(percent_food / 100 * area)
        number_shelter_cells = math.floor(percent_shelter / 100 * area)
        # if the calculations produced more or less of the squares needed, this should clean it up.
        # there shouldn't be more than three cells difference because of how I rounded it, so this shouldn't
        # affect the final result much
        distro = area - (number_crop_cells + number_food_cells + number_shelter_cells)
        # I'll prioritize adding shelter cells if they elected to have them, or else I'll add food cells
        # I feel like most farmers would prioritize wind breaks over feeding butterflies
        while distro > 0:
            if number_shelter_cells > 0:
                number_shelter_cells += 1
            else:
                number_food_cells += 1
            distro = area - (number_crop_cells + number_food_cells + number_shelter_cells)
        # If there are any food cells, remove those first, then shelter cells
        while distro < 0:
            if number_food_cells > 0:
                number_food_cells -= 1
            else:
                number_shelter_cells -= 1
            distro = area - (number_crop_cells + number_food_cells + number_shelter_cells)
        try:
            distro == 0
        except ValueError:
            print('something went wrong in the cell calculations')
            sys.exit(1)
        random_f = np.full((length, width), 1, dtype=int).tolist()
        while number_shelter_cells + number_food_cells > 0:
            if number_shelter_cells > 0:
                temp_length = np.random.randint(0, length - 1)
                temp_width = np.random.randint(0, width - 1)
                if random_f[temp_length][temp_width] == 1:
                    random_f[temp_length][temp_width] = 3
                    number_shelter_cells -= 1
            if number_food_cells > 0:
                temp_length = np.random.randint(0, length - 1)
                temp_width = np.random.randint(0, width - 1)
                if random_f[temp_length][temp_width] == 1:
                    random_f[temp_length][temp_width] = 2
                    number_food_cells -= 1
        return cls(random_f)