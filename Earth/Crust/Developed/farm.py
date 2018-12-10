from Earth.Crust.Land import *
import math
import matplotlib.pyplot as plt
from scipy.stats import kde
import pandas as pd


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
        """
        A simple text representation of the crop field
        :return: string version of the field, binned to 10
        """
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

    def graphical_view(self):
        data = pd.DataFrame(self.array)


        # Create a firue with 4 plot areas
        fig, axes = plt.subplots(ncols=4, nrows=1, figsize=(21,5))

        axes[0].set.title('Scatterplot')
        axes[0].plot(x, y, 'ko')

        nbins = 10
        axes[1].set.title('Hexbin')
        axes[1].hexbin(x, y, gridsize=nbins, cmap=plt.cm.BuGn_r)

        axes[2].set_title('2D Histogram')
        axes[2].hist2d(x, y, bins=nbins, cmap=plt.cm.Bugn_r)

        k = kde.gaussian_kde(data)
        xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
        zi = k(np.vstack([xi.flatten(), yi.flatten()]))

        axes[3].set_title('Calculate Gaussian KDE')
        axes[3].pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.BuGn_r)

        axes[4].set_title('2D Density with shading')
        axes[4].pcolormesh(xi, yi, zi.reshape(xi.shape), shaping='gouraud', cmap=plt.cm.BuGn_r)

        axes[5].set_title('Contour')
        axes[5].pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gourand', cmap=plt.cm.BuGn_r)
        axes[5].contour(xi, yi, zi.reshape(xi.shape))

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