import numpy as np
import sys
import math
import time


class Area:
    """
    A generic area, consisting of a length and width, 1 unit of length = 1 unit of
    width = 15 meters. This will form the basis of the CropField class. It takes a two-dimensional array
    as an input and converts it into a numpy array, then checks that it is a true 2D array (a list of lists,
    with all sublists being the same length)
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
        values = [1, 2, 3]
        if False in np.isin(self.array, values):
            raise ValueError("Values of CropField must be either 1 (crop), 2 (food), or 3 (shelter)")
        ix_food = np.isin(self.array, 2)
        self.food_indices = []
        if True in ix_food:
            self.food_indices = list(zip(np.where(ix_food)[0], np.where(ix_food)[1]))
        ix_shelter = np.isin(self.array, 3)
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
                else:
                    print("values must be either 1 (crop), 2 (food), or 3 (shelter)")
            if row != self.row_len:
                string_version += '\n'
        return string_version

    def __str__(self) -> str:
        return self.__to_string()

    def __repr__(self) -> str:
        return self.__to_string()

    def raw(self):
        string_version = ''
        for row in range(self.row_len):
            for column in range(self.col_len):
                string_version += str(self.array[row][column])
                if column != self.col_len-1:
                    string_version += " "
            if row != self.row_len:
                string_version += '\n'
        print(string_version)

    @classmethod
    def random_field(cls, length, width, percent_crops=100, percent_food=0, percent_shelter=0):
        # creates a random field given the dimensions. Picks placement of food and shelter randomly
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


class Pollinator:
    """
    Generic Pollinator class which the others will be based on. All animals are tied to an area, so there must be an
    area first to have an animal
    """
    def __init__(self, area: Area):
        # Pollinators start out alive with a random amount of food
        self.food_level = float(np.random.randint(0, 101))
        self.status = "alive"
        self.area_length = area.shape[0]
        self.area_width = area.shape[1]
        self.area = area
        self.position = [0, 0]

    def __str__(self):
        return '{} with {:.2f}% food at {}'.format(type(self).__name__, self.food_level, self.position)

    def __repr__(self):
        return '{} with {:.2f}% food at {}'.format(type(self).__name__, self.food_level, self.position)

    def check_for_death(self):
        # Based on how much food it currently has, the Pollinator's chances to die randomly change. If it drops below
        # a near-zero threshold it dies automatically
        roll_die = np.random.random_sample()
        if self.food_level > 80:
            if roll_die < 0.000001:
                self.status = 'dead'
                return self
            else:
                return self
        elif self.food_level > 50.0:
            if roll_die < 0.0001:
                self.status = 'dead'
                return self
            else:
                return self
        elif 25.0 < self.food_level <= 50.0:
            if roll_die <= 0.001:
                self.status = 'dead'
                return self
            else:
                return self
        elif 1.0 <= self.food_level <= 25.0:
            if roll_die < 0.01:
                self.status = 'dead'
                return self
            else:
                return self
        elif self.food_level < 1.0:
            if roll_die < 0.5:
                self.status = 'dead'
                return self
        else:
            self.status = 'dead'
            return self

    def random_move(self):
        # The pollinator moves randomly
        coord = np.random.choice((0, 1))
        direction = np.random.choice((-1, 1))
        if coord == 0:
            # Move north-south
            if self.area_length - 1 > self.position[0] > 0:
                self.position[coord] += direction
            else:
                self.check_for_death()
        else:
            # Move east-west
            if self.area_width - 1 > self.position[1] > 0:
                self.position[1] += direction
            else:
                self.check_for_death()
        return self


class Monarch(Pollinator):
    """
    This class creates the Monarch butterfly object. The monarch is modeled as migrating north. It's movement is
    mainly north, unless it is seeking food or shelter. It will seek shelter when night approaches and food when it is
    hungry, unless it is sheltered. It enters on the edge of the field in a random position. It also has an element of
    randomness to it's movement, as wind currents can blow the insect off course.
    >>> f = CropField([[1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1]])
    >>> b1 = Monarch(f)
    >>> b1.food_level = 100
    >>> b1.position = [1,3]
    >>> print(b1.food_level)
    100
    >>> b1.position
    [1, 3]
    >>> b1
    Monarch with 100% food at [1, 3]

    """

    def __init__(self, area: CropField):
        Pollinator.__init__(self, area)
        self.sheltered = True
        self.food_indices = area.food_indices
        self.shelter_indices = area.shelter_indices
        # This gives the starting position
        variable = np.random.choice([0, 0, 0, 0, 0, 1, 2, 3])
        if variable == 0:
            self.position = [self.area_length - 1, np.random.randint(self.area_width)]
        elif variable == 1:
            self.position = [np.random.randint(int(self.area_length/2)), 0]
        elif variable == 2:
            self.position = [np.random.randint(int(self.area_length/2)), self.area_width-1]
        else:
            if self.shelter_indices:
                self.position = list(self.shelter_indices[np.random.choice(len(self.shelter_indices))])
            else:
                self.position = [self.area_length - 1, np.random.randint(self.area_width)]

    def move_one_day(self, seconds=0, hours=4):
        """
        This is a long bunch of loops and if statements that basically amount to: move north unless you are hungry,
        in which case move toward food. Every once in awhile move toward shelter (rain simulation)
        One day is 86400 seconds. The day begins at 4 am, which should be light everywhere with in
        the monarch's range in the spring/summer when it is moving north. Because we are assuming that the
        butterfly covers this amount of distance in a day, One unit of movement thus represents about 26 seconds.
        This accounts for all the random fluttering and stopping that a butterfly does as it traverses 15 meters.
        Therefore, the counter will increase 25 seconds per loop (to simplify the math). Night wil be assumed 
        to start at 9pm, giving it 17 hours of day and 7 hours of night. During the night it will prioritize 
        seeking shelter. To allow for multiple butterflies, Seconds and hours will be an input into this 
        method.
        TODO: More than one butterfly will attempt to group together for shared warmth.
        :param hours: current number of seconds
        :param seconds: current hours
        :return: the Monarch object, appropriately manipulated
        """
        # seconds = 0
        # hour = 4 # keeping these here for reference for now
        flag = False
        while self.status == 'alive':
            # this is a check to enusure we are modeling the day from 4am to 4 am. If this particulare butterfly
            # enters the day a little later than the others, it will synrchronize to the same schedule.
            if flag:
                return self, seconds, hours
            if seconds == 3600:
                hours += 1
                seconds = 0  # reset counter for the next hour
                # at midnight the 24-clock cycles back around to 0
                if hours == 24:
                    hours = 0
            # if this is the last loop of the day, then we set the flag
            if seconds == 3575 and hours == 3:
                flag = True
            # If it's daylight, the priorities will be food and moving north. It may randomly occasionally seek shelter
            # if it happens to be near a tree.
            if 4 <= hours < 21:
                # always good to make sure the damn thing is still alive before we do all this work
                self.check_for_death()
                if self.status == 'dead':
                    return self, seconds, hours
                # If it's in shelter during the day light, there's a small chance it will just stay put, unless
                # it is super hungry
                if self.sheltered:
                    # Just a check to make sure it is actually in a tree area and marked as sheltered...
                    if self.area.array[self.position[0]][self.position[1]] != '*':
                        self.sheltered = False
                    roll_die = np.random.random_sample()
                    if self.food_level < 25:
                        self.sheltered = False
                        self.random_move()
                    elif roll_die < 0.99:
                        self.sheltered = False
                    else:
                        pass
                    if self.food_level > 0.0112:
                        self.food_level -= 0.0112
                    else:
                        self.food_level = 0
                    # I had to add in a lot of death checks because I was having a bunch of zombie butterflies in my sim
                    # While it is no longer in shelter, it will be the next cycle before it starts moving again.
                    # Also, maybe it just plain died.
                    self.check_for_death()
                    if self.status == 'dead':
                        return self, seconds, hours
                else:
                    if self.status == 'dead':
                        return self, seconds, hours

                    # Above a 50% food level, we'll consider it full
                    if self.food_level >= 50.0:
                        # Pick a random number
                        roll_die = np.random.random_sample()
                        # first decrement it's food level
                        if self.food_level > 0.0225:
                            self.food_level -= 0.0225
                        else:
                            # to account for rounding errors anything less than 0.0225 is just 0
                            self.food_level = 0
                            self.check_for_death()
                            if self.status == 'dead':
                                return self, seconds, hours
        
                        # Usually, it will try to move north
                        if roll_die <= 0.9:
                            # If it's anywhere on the map but the top row, move north one, or maybe randomly
                            if self.area_length > self.position[0] > 0:
                                second_die = np.random.random_sample()
                                if second_die > 0.005:
                                    self.position[0] -= 1
                                else:
                                    self.random_move()
                                if self.status == 'dead':
                                    return self, seconds, hours

                            # if its in the top row, it will try to leave
                            elif self.position[0] == 0:
                                second_die = np.random.random_sample()
                                # Maybe it dies trying to leave
                                if second_die > 0.01:
                                    self.check_for_death()
                                    if self.status == 'dead':
                                        return self, seconds, hours
                                    else:
                                        # You survived buddy!
                                        self.status = "exit"
                                        return self, seconds, hours
                                else:
                                    self.random_move()
                                    if self.status == 'dead':
                                        return self, seconds, hours
                            else:
                                # if it has somehow gone off the map, I'll just mark it as gone.
                                self.status = 'exit'
                                return self, seconds, hours
                        elif 0.9 < roll_die <= 0.925:
                            # Easterly
                            second_die = np.random.random_sample()
                            # if moving east doesn't take it off the map, move east
                            if second_die > 0.001 and self.position[1] < self.area_width - 1:
                                self.position[1] += 1
                            # If it's on the eastern edge, there's a slight chance it exits
                            elif 0.0001 <= second_die <= 0.001 and self.position == self.area_width - 1:
                                self.check_for_death()
                                if self.status == 'dead':
                                    return self, seconds, hours
                                else:
                                    self.status = 'exit'
                                    return self, seconds, hours
                            else:
                                # And a slight chance it just does nothing
                                self.check_for_death()
                                if self.status == 'dead':
                                    return self, seconds, hours
                        elif 0.925 < roll_die <= 0.95:
                            # Southerly
                            second_die = np.random.random_sample()
                            # if there's any room to the south it will try to move south
                            if second_die > 0.001 and self.position[0] < self.area_length - 1:
                                self.position[0] += 1
                            else:
                                # or it will just wait
                                self.check_for_death()
                                if self.status == 'dead':
                                    return self, seconds, hours
                        elif 0.95 < roll_die <= 0.975:
                            # Westerly
                            second_die = np.random.random_sample()
                            # If there's room, it will move west
                            if second_die > 0.001 and self.position[1] > 0:
                                self.position[1] -= 1
                            # If it's on the west edge, there's a slight change it will simple leave
                            elif 0.0001 <= second_die <= 0.001 and self.position == 0:
                                self.check_for_death()
                                if self.status == 'dead':
                                    return self, seconds, hours
                                else:
                                    self.status = 'exit'
                                    return self, seconds, hours
                            else:
                                # if not, it just waits
                                self.check_for_death()
                                if self.status == 'dead':
                                    return self, seconds, hours
        
                    # if it's a little hungry, it may seek food
                    elif 25.0 <= self.food_level < 50.0:
                        roll_die = np.random.random_sample()
                        if roll_die <= 0.001:
                            # slight chance of moving randomly instead
                            self.random_move()
                            if self.status == 'dead':
                                return self, seconds, hours
                        else:
                            # usually look for food
                            self.seek_resource('food')
                            if self.status == 'dead':
                                return self, seconds, hours
        
                    # now it's very hungry and will almost certainly seek food
                    else:
                        roll_die = np.random.random_sample()
                        # slight chance it moves randomly
                        if roll_die <= 0.0001:
                            self.random_move()
                            if self.status == 'dead':
                                return self, seconds, hours
                        # otherwise look for food
                        else:
                            self.seek_resource('food')
                            if self.status == 'dead':
                                return self, seconds, hours
        
                    # now that it has moved, if it's near shelter, there's a small chance it may take shelter
                    if self.area.array[self.position[0]][self.position[1]] == 3:
                        roll_die = np.random.random_sample()
                        if roll_die >= .99:
                            self.sheltered = True
        
                    # if it's near food, it will most likely try to eat
                    if self.area.array[self.position[0]][self.position[1]] == 2:
                        roll_die = np.random.random_sample()
                        if roll_die <= .95:
                            self.food_level = 100

            # During the evening, it will prioritize seeking shelter. It will stay in shelter through the night
            # once it locates it, so we'll remove the leave shelter component of the checks. There's no real 
            # food to be had at night, so we'll just assume it battens down the hatches. If it's food falls too low
            # it may die. Such is the risk of life.
            if 21 <= hours < 24 or 0 <= hours < 4:
                # Quick check to make sure it is still alive before we do all this work
                self.check_for_death()
                if self.status == 'dead':
                    return self, seconds, hours
                if self.sheltered and self.status == 'alive':
                    # At night it will batten down the hatches and stay sheltered
                    # If for whatever reason it is marked as sheltered but isn't in a tree...
                    if self.area[self.position[0]][self.position[1]] != '*':
                        self.sheltered = False
                    # Resting conserves food reserves
                    self.food_level -= 0.0112
                    self.check_for_death()
                    if self.status == 'dead':
                        return self, seconds, hours
                else:
                    # otherwise it's going to look for shelter
                    self.seek_resource('shelter')
                    if self.status == 'dead':
                        return self, seconds, hours

                    # now that it has moved, if it's near shelter, it make take shelter
                    if self.area.array[self.position[0]][self.position[1]] == 3:
                        roll_die = np.random.random_sample()
                        if roll_die >= .9:
                            self.sheltered = True

                    # if it's near food, it will may try to eat
                    elif self.area.array[self.position[0]][self.position[1]] == 2:
                        roll_die = np.random.random_sample()
                        if roll_die >= .9:
                            self.food_level = 100
            seconds += 25
        return self, seconds, hours

    def seek_resource(self, resource):
        # Let's make sure no zombie butterflies are looking for our resources
        if self.status == 'dead':
            return self

        if resource == 'shelter':
            if not self.shelter_indices:
                # There's no shelter, so it just wanders :(
                self.random_move()
                return self
            else:
                if tuple(self.position) in self.shelter_indices:
                    nearest = tuple(self.position)
                else:
                    nearest = min(self.shelter_indices, key=lambda x: distance(x, self.position))

        elif resource == 'food':
            if not self.food_indices:
                # There's no food, so it just wanders :(
                self.random_move()
                return self
            else:
                if tuple(self.position) in self.food_indices:
                    nearest = tuple(self.position)
                else:
                    nearest = min(self.food_indices, key=lambda x: distance(x, self.position))

        else:
            raise ValueError('incorrect resource passed to seek_resource function')

        # There's a random chance it can't reach the resource, otherwise it does
        # and spends the appropriate amount of energy to get there
        die_roll = np.random.random_sample()
        if die_roll >= 0.001:
            self.food_level -= distance(self.position, nearest) * 0.0225
            if self.food_level < 0:
                self.food_level = 0
            self.position = list(nearest)
            self.check_for_death()
            if self.status == 'dead':
                return self
            if resource == 'food':
                self.food_level = 100
            else:
                self.sheltered = True
            return self

        # Moves randomly instead of seeking resource. Better luck next time.
        else:
            self.random_move()
            self.food_level -= 0.0225
            return self


def distance(x: list, y: tuple) -> int:
    return abs(x[0]-y[0]) + abs(x[1]-y[1])


def create_standard_test(iterations: int) -> CropField:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
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
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for j in range(98):
        standard_field.append(base_field_middle_rows)
    standard_field.append(base_field_bottom_rows)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return CropField(construction)


def create_food_heavy_test(iterations: int) -> CropField:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
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
    return CropField(construction)


def create_shelter_heavy_test(iterations: int) -> CropField:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
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
    return CropField(construction)


def create_middle_food_windbreak_test(iterations: int) -> CropField:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
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
    return CropField(construction)


def create_middle_shelter_windbreak_test(iterations: int) -> CropField:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
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
    return CropField(construction)


def create_test_food_test(iterations: int) -> CropField:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
    # create the top and bottom row_len of the field
    base_field_base_rows = [2] * 100
    # Build up a single standard field
    standard_field = [base_field_base_rows]
    for j in range(0, 98):
        standard_field.append(base_field_base_rows)
    standard_field.append(base_field_base_rows)
    # create the standard test site
    construction = []
    for j in range(0, iterations + 1):
        construction += standard_field
    return CropField(construction)


def create_middle_shelter_windbreak_test_2(iterations: int) -> CropField:
    # fields are assumed to have a scale 1 cell has dimension 15 meters x 15 meters
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
    return CropField(construction)


def test_field(dictionary, number):
    # This function takes care of some repetitive code I had written earlier. It's not perfect, but it works for now.
    start_time = time.time()
    if number == 0:
        field_to_test = create_standard_test(33)
    elif number == 1:
        field_to_test = create_food_heavy_test(33)
    elif number == 2:
        field_to_test = create_middle_food_windbreak_test(33)
    elif number == 3:
        field_to_test = create_middle_shelter_windbreak_test(33)
    elif number == 4:
        field_to_test = create_shelter_heavy_test(33)
    elif number == 5:
        field_to_test = CropField.random_field(3333, 100, 90, 5, 5)
    elif number == 6:
        field_to_test = CropField.random_field(3333, 100, 80, 15, 5)
    elif number == 7:
        field_to_test = CropField.random_field(3333, 100, 80, 5, 15)
    else:
        return dictionary
    results = []
    for j in range(1000):
        monarch1 = Monarch(field_to_test)
        monarch1.move_one_day()
        results.append(monarch1.get_status())
    dictionary["test_field_{}".format(number)] = [100 * results.count('exit') / len(results)]
    print("Dead percentage = {:.2f}%".format(100 * results.count('dead') / len(results)))
    print("Exit percentage = {:.2f}%".format(100 * results.count('exit') / len(results)))
    print("--- %s seconds ---" % (time.time() - start_time))
    return dictionary


def main():
    # This is a field of only food, to test the parameters
    starttime = time.time()
    testfield = create_test_food_test(33)
    print(testfield.row_len*15, testfield.col_len*15)
    print(testfield)
    results = []
    print('starting test')
    for k in range(1000):
        monarch1 = Monarch(testfield)
        monarch1, seconds, hours = monarch1.move_one_day()
        results.append(monarch1.status)
    print("Dead percentage = {:.2f}%".format(100 * results.count('dead') / len(results)))
    print("Exit percentage = {:.2f}%".format(100 * results.count('exit') / len(results)))
    print("--- %s seconds ---" % (time.time() - starttime))


if __name__ == '__main__':
    main()
    # first analysis
    # master_results = {}
    # for i in range(0, 8):
    #     test_field(master_results, i)
    # index = ['standard', 'food_heavy', 'middle_food', 'middle_shelter', 'shelter_heavy', 'balanced_random',
    #           'food_random', 'shelter_random']
    # master_results = pd.DataFrame(master_results).T
    # master_results.index = index
    # print("The best-performing field was {}".format(master_results[0].idxmax()))

    # field stats
    # field = create_middle_shelter_windbreak_test(333)
    # food = len(field[field == 'o'].stack().index.tolist())
    # shelter = len(field[field == '*'].stack().index.tolist())
    # crops = len(field[field == '='].stack().index.tolist())
    # total = food + shelter + crops
    # print('Percent food: {:.2f}%'.format(math.ceil(100 * food/total)))
    # print("Percent shelter: {:.2f}%".format(math.ceil(100 * shelter/total)))
    # print("Percent crops: {:.2f}%".format(math.floor(100 * crops/total)))

    # try to find an optimal random field
    # start_time = time.time()
    # score_dictionary = {}
    # for i in range(1000):
    #     field = CropField.random_field(3333, 100, 95, 4, 1)
    #     food_indices = create_food_table(field)
    #     shelter_indices = create_shelter_table(field)
    #     results = []
    #     for j in range(200):
    #         monarch1 = Butterfly(field)
    #         monarch1.move_one_day()
    #         results.append(monarch1.get_status())
    #     score_dictionary["test_field_{}".format(i)] = [(100 * (results.count('exit') / len(results))), field]
    #     print("--- %s seconds ---" % (time.time() - start_time))
    # df = pd.DataFrame(score_dictionary).T
    # print(df.loc[df[0].idxmax()][0])
    # print(df.loc[df[0].idxmax()][1])

    # Testing a higher crop percentage variant of the middle row_len
    # start_time = time.time()
    # field_test = create_middle_shelter_windbreak_test_2(333)
    # food_indices = create_food_table(field_test)
    # shelter_indices = create_shelter_table(field_test)
    # results = []
    # for j in range(100):
    #     monarch1 = Butterfly(field_test)
    #     monarch1.move_one_day()
    #     results.append(monarch1.get_status())
    # print("Dead percentage = {:.2f}%".format(100 * results.count('dead') / len(results)))
    # print("Exit percentage = {:.2f}%".format(100 * results.count('exit') / len(results)))
    # print("--- %s seconds ---" % (time.time() - start_time))
    #
    # food = len(field_test[field_test == 'o'].stack().index.tolist())
    # shelter = len(field_test[field_test == '*'].stack().index.tolist())
    # crops = len(field_test[field_test == '='].stack().index.tolist())
    # total = food + shelter + crops
    # print('Percent food: {:.2f}%'.format(math.ceil(100 * food/total)))
    # print("Percent shelter: {:.2f}%".format(math.ceil(100 * shelter/total)))
    # print("Percent crops: {:.2f}%".format(math.floor(100 * crops/total)))

    
