from Land_Use.Land import *
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
        return '{} m x {} m'.format(self.row_len * 15, self.col_len * 15)

    def __repr__(self) -> str:
        return '{} m x {} m'.format(
            self.row_len * 15, self.col_len * 15)

    # def graphical_view(self):
    #     data = pd.DataFrame(self.array)
    #
    #
    #     # Create a firue with 4 plot areas
    #     fig, axes = plt.subplots(ncols=4, nrows=1, figsize=(21,5))
    #
    #     axes[0].set.title('Scatterplot')
    #     axes[0].plot(x, y, 'ko')
    #
    #     nbins = 10
    #     axes[1].set.title('Hexbin')
    #     axes[1].hexbin(x, y, gridsize=nbins, cmap=plt.cm.BuGn_r)
    #
    #     axes[2].set_title('2D Histogram')
    #     axes[2].hist2d(x, y, bins=nbins, cmap=plt.cm.Bugn_r)
    #
    #     k = kde.gaussian_kde(data)
    #     xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
    #     zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    #
    #     axes[3].set_title('Calculate Gaussian KDE')
    #     axes[3].pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.BuGn_r)
    #
    #     axes[4].set_title('2D Density with shading')
    #     axes[4].pcolormesh(xi, yi, zi.reshape(xi.shape), shaping='gouraud', cmap=plt.cm.BuGn_r)
    #
    #     axes[5].set_title('Contour')
    #     axes[5].pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gourand', cmap=plt.cm.BuGn_r)
    #     axes[5].contour(xi, yi, zi.reshape(xi.shape))

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

# The following are a collection of pre-defined fields that made sense to test. More can be added by constructing the
# field in a similar manner. One could also think of 'crop' land as generic "developed area' and use the same basic
# template to construct urban models
class StandardTest(CropField):
    """
    Standard test field. This is multiple iterations of 1 acre fields arranged with buffors along the borders, basically
    wind breaks with some food along the border.
    """

    def __init__(self, iterations):
        # Create the base array:
        # create the top row of the field
        base_field_base_rows = [2] * 100
        base_field_base_rows[0] = 3
        base_field_base_rows[99] = 3
        # create the bottom row_len of the field
        base_field_bottom_rows = [3] * 100
        # create the standard middle row
        base_field_middle_rows = [1] * 100
        base_field_middle_rows[0] = 3
        base_field_middle_rows[99] = 3
        # Build up a single standard acre field
        standard_field = [base_field_base_rows]
        for j in range(98):
            standard_field.append(base_field_middle_rows)
        standard_field.append(base_field_bottom_rows)
        # create the standard test site\
        construction = []
        for j in range(0, iterations + 1):
            construction += standard_field
        CropField.__init__(self, construction)

    def __str__(self) -> str:
        return 'Standard Field Test'

    def __repr__(self) -> str:
        return 'Standard Field Test'


class HeavyFoodTest(CropField):
    """
    food heavy test field
    This field has a southern windbreak along the edges with food-type wild plants along the east and west sides and
    breaking up each section along the middle. The idea being give the butterfly an avenue of food on the edges to work
    its way north
    """
    def __init__(self, iterations):
        # create the top and bottom row_len of the field
        base_field_base_rows = [2] * 100
        # create the standard middle row
        base_field_middle_rows = [1] * 100
        base_field_middle_rows[0] = 2
        base_field_middle_rows[99] = 2
        base_bottom_row = [3] * 100
        # Build up a single standard field
        standard_field = [base_field_base_rows]
        for j in range(0, 98):
            standard_field.append(base_field_middle_rows)
        standard_field.append(base_bottom_row)
        # create the standard test site
        construction = []
        for j in range(0, iterations + 1):
            construction += standard_field
        CropField.__init__(self, construction)

    def __str__(self) -> str:
        return 'Food Heavy Test'

    def __repr__(self) -> str:
        return 'Food Heavy Test'


class ShelterHeavyTest(CropField):
    """
    Shelter heavy test field
    This field features a break in the middle running east-west that provides shelter and food along the edges. The idea
    being that they might need a break when they get halfway.
    """
    def __init__(self, iterations):
        # create the top and bottom row_len of the field
        base_field_base_rows = [3] * 100
        base_field_base_rows[0] = 3
        base_field_base_rows[99] = 3
        # create the standard middle row
        base_field_middle_rows = [1] * 100
        base_field_middle_rows[0] = 2
        base_field_middle_rows[99] = 2
        # Build up a single standard field
        standard_field = [base_field_base_rows]
        for j in range(0, 98):
            standard_field.append(base_field_middle_rows)
        standard_field.append(base_field_base_rows)
        # create the standard test site
        construction = []
        for j in range(0, iterations + 1):
            construction += standard_field
        CropField.__init__(self, construction)

    def __str__(self) -> str:
        return 'Shelter Heavy Test'

    def __repr__(self) -> str:
        return 'Shelter Heavy Test'


class MiddleFoodWindbreakTest(CropField):
    """
    Food on the borders with a windbreak down the middle
    In my simulations, this has been the most successful. It has food along the middle running north/south, trees around
    the borders and a row of trees running east-west in the middle. The idea being that wherever the butterfly finds
    itself initially, it is always fairly close to food. The trees in the middle provide shelter at night.
    """
    def __init__(self, iterations):
        # create the top and bottom row_len of the field
        base_field_base_rows = [3] * 100
        # create the standard middle row
        base_field_middle_rows = [1] * 100
        base_field_middle_rows[0] = 3
        base_field_middle_rows[99] = 3
        base_field_middle_rows[49] = 2
        # Build up a single standard field
        standard_field = [base_field_base_rows]
        for j in range(0, 98):
            standard_field.append(base_field_middle_rows)
        standard_field.append(base_field_base_rows)
        # create the standard test site
        construction = []
        for j in range(0, iterations + 1):
            construction += standard_field
        CropField.__init__(self, construction)

    def __str__(self) -> str:
        return 'Food Heavy Middle Windbreak'

    def __repr__(self) -> str:
        return 'Food Heavy Middle Windbreak'


class MiddleShelterWindbreakTest(CropField):
    """
    Shelter heavy middle windbreak test field
    Similar to above, but with food on the outside, trees in the middle
    """
    def __init__(self, iterations):
        # create the top and bottom row_len of the field
        base_field_base_rows = [2] * 100
        # create the standard middle row
        base_field_middle_rows = [1] * 100
        base_field_middle_rows[0] = 2
        base_field_middle_rows[99] = 2
        base_field_middle_rows[49] = 3
        # Build up a single standard field
        standard_field = [base_field_base_rows]
        for j in range(0, 98):
            standard_field.append(base_field_middle_rows)
        standard_field.append(base_field_base_rows)
        # create the standard test site
        construction = []
        for j in range(0, iterations + 1):
            construction += standard_field
        CropField.__init__(self, construction)

    def __str__(self) -> str:
        return 'Shelter heavy middle windbreak'

    def __repr__(self) -> str:
        return 'Shelter heavy middle windbreak'


class FallowTest(CropField):
    """
    Fallow test field
    A field entirely of food that has been left to go fallow for the season. Farmers often do this to help recover
    nitrogen in the soil. The columns of food go every other row
    """
    def __init__(self, iterations):
        # create the top and bottom row_len of the field
        base_field_base_rows = [4] * 100
        base_field_base_rows[0] = 3
        base_field_base_rows[99] = 3
        # Build up a single standard field
        standard_field = [base_field_base_rows]
        for j in range(0, 98):
            standard_field.append(base_field_base_rows)
        standard_field.append(base_field_base_rows)
        # create the standard test site
        construction = []
        for j in range(0, iterations + 1):
            construction += standard_field
        CropField.__init__(self, construction)

    def __str__(self) -> str:
        return 'Fallow test field'

    def __repr__(self) -> str:
        return 'Fallow test field'


class MiddleShelterWindbreakTest2(CropField):
    """
    Shelter heavy middle windbreak test field 2
    Like the previous, but the line of food is unbroken.
    """
    def __init__(self, iterations):
        # create the top and bottom row_len of the field
        base_field_base_rows = [2] * 100
        # create the standard middle row
        base_field_middle_rows = [1] * 100
        base_field_middle_rows[0] = 2
        base_field_middle_rows[99] = 2
        base_field_middle_rows[49] = 3
        base_field_middle_rows_variant = [1] * 100
        base_field_middle_rows_variant[49] = 3
        # Build up a single standard field
        standard_field = [base_field_base_rows]
        for j in range(0, 24):
            standard_field.append(base_field_middle_rows_variant)
            standard_field.append(base_field_middle_rows_variant)
            standard_field.append(base_field_middle_rows)
            standard_field.append(base_field_middle_rows)
        standard_field.append(base_field_middle_rows_variant)
        standard_field.append(base_field_base_rows)
        # create the standard test site
        construction = []
        for j in range(0, iterations + 1):
            construction += standard_field
        CropField.__init__(self, construction)

    def __str__(self) -> str:
        return 'Shelter heavy windbreak middle 2'

    def __repr__(self) -> str:
        return 'Shelter heavy windbreak middle 2'


