#!/home/joshua/anaconda3/bin/python


import numpy as np
import math
import time
import pandas as pd
import copy
import sys
import pickle


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
        return '{} m x {} m area'.forma


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
            raise ValueError("Values of CropField must be either 1 (crop), 2 (food), 3 (shelter), or 4 (mixed food and shelter)")
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

    __food_unit = 0.5
    __death_factor = 0.5
    __exit_chance = 0
    # Some pollinators will try to exit if they are near the edge
    __can_exit_north = False
    # Others will only exit if on the north edge (e.g., monarchs)
    __can_exit = False
    __shelter_chance = 0.5

    def __init__(self, area: Area):
        # Pollinators start out alive with a random amount of food
        self.food_level = float(int(np.random.normal(50, scale=15)))
        if self.food_level < 0.0:
            self.food_level = 0.0
        elif self.food_level > 100.0:
            self.food_level = 100.0
        self.status = "alive"
        self.cause_of_death = ""
        self.area_length = area.shape[0]
        self.area_width = area.shape[1]
        self.area = area
        self.position = [0, 0]
        self.sheltered = False
        self.food_indices = area.food_indices
        self.shelter_indices = area.shelter_indices
        # Initialize an empty moves list. This will be a record of this pollinator
        self.ways_to_die = ['Eaten by a bird', 'Impaled on a thorn', 'Death by disease', 'Run over by a tractor']
        # This defines the starting time of the pollinator. For the simualtion, the inital time will start a 4 am,
        # which is roughly sunup in the midwest in the summer. But other pollinators that enter may enter at different
        # tims, so I'll leave it open.
        self.days = 0
        self.hours = 4
        self.seconds = 0
        self.turns = 0

    def __str__(self):
        return '{} with {:.2f}% food at {}, status: {}'.format(type(self).__name__, self.food_level, self.position,
                                                               self.status)

    def __repr__(self):
        return '{} with {:.2f}% food at {}, status: {}'.format(type(self).__name__, self.food_level, self.position,
                                                               self.status)

    def kill_it(self):
        self.status = 'dead'
        self.cause_of_death = np.random.choice(self.ways_to_die)
        return self

    def check_for_death(self):
        # Based on how much food it currently has, the Monarch's chances to die randomly change.
        roll_die = np.random.random_sample()
        if self.food_level > 90 and roll_die < self.__class__.__death_factor/1000:
            self.kill_it()
            return self
        elif 50.0 < self.food_level <= 90 and roll_die < self.__class__.__death_factor/100:
            self.kill_it()
            return self
        elif 25.0 < self.food_level <= 50.0 and roll_die <= self.__class__.__death_factor:
            self.kill_it()
            return self
        elif 0.01 <= self.food_level <= 25.0 and roll_die < self.__class__.__death_factor * 50:
            self.kill_it()
            return self
        elif self.food_level < 0.01 and roll_die < self.__class__.__death_factor * 99:
            self.status == 'dead'
            print('Starved to death')
            return self
        else:
            return self

    def decrement_food(self, amount):
        if self.food_level >= amount:
            self.food_level -= amount
        else:
            self.food_level = 0
        return self

    def check_if_exit(self):
        if (self.__class__.__can_exit_north or self.__class__.__can_exit) and self.position[0] == 0:
            self.status = np.random.choice(['exit', 'alive'], p=[self.__class__.__exit_chance, 1-self.__class__.__exit_chance])

        elif self.__class__.__can_exit and (self.position[0] == self.area_length-1 or
                                          self.position[1] == 0 or self.position[1] == self.area_width-1):
            self.status = np.random.choice(['exit', 'alive'], p=[self.__class__.__exit_chance, 1-self.__class__.__exit_chance])

        elif (self.position[0] < 0 or self.position[0] > self.area_length - 1 or
              self.position[1] < 0 or self.position[1] > self.area_width - 1):
            # If it can exit and it's wandered off the map, just mark it as gone
            if self.__class__.__can_exit or self.__class__.__can_exit_north:
                self.status = 'exit'
            else:
                x = np.random.randint(0, self.area_length - 1)
                y = np.random.randint(0, self.area_width - 1)
                self.record_moves(x, y)
                self.food_level = self.food_level / 2

    def record_moves(self, x, y):
        if x > self.position[0]:
            for i in range(abs(self.position[0] - x)):
                self.position[0] += 1
                self.moves.append(copy.deepcopy(self.position))
        elif x < self.position[0]:
            for i in range(abs(self.position[0] - x)):
                self.position[0] -= 1
                self.moves.append(copy.deepcopy(self.position))
        else:
            pass
        if y > self.position[1]:
            for j in range(abs(self.position[1] - y)):
                self.position[1] += 1
                self.moves.append(copy.deepcopy(self.position))
        elif y < self.position[1]:
            for i in range(abs(self.position[1] - y)):
                self.position[1] -= 1
                self.moves.append(copy.deepcopy(self.position))
        else:
            pass

    def random_move(self, number: int = 1):
        self.check_if_exit()
        if self.status == 'exit':
            return self

        # Standard random move
        for i in range(number):
            coord = np.random.choice((0, 1))
            direction = np.random.choice((-1, 1))
            if coord == 0:
                # Move north-south
                if self.area_length -1 > self.position[0] > 0:
                    self.position[coord] += direction
                    self.decrement_food(self.__class__.__food_unit)
                    self.moves.append(copy.deepcopy(self.position))
                else:
                    pass
            else:
                # Move east-west
                if self.area_width - 1 > self.position[1] > 0:
                    self.position[1] += direction
                    self.decrement_food(self.__class__.__food_unit)
                    self.moves.append(copy.deepcopy(self.position))
                else:
                    pass

    def simple_move(self, direction: str = 'north'):
        """
        This method simply moves the monarch one unit in one direction. It's specific to the butterfly because
        it will try to leave if it is on the northernmost border. Other pollinators might not behave this way
        :param direction: A string giving the ordinal direction
        :return: simple returns the updated butterfly
        >>> testfield = CropField.random_field(100,100,90,5,5)
        >>> b1 = Monarch(testfield)
        >>> b1.simple_move("worst")
        Traceback (most recent call last):
          File "C:\Program Files\JetBrains\PyCharm 2018.2.3\helpers\pycharm\docrunner.py", line 140, in __run
            compileflags, 1), test.globs)
          File "<doctest simple_move[2]>", line 1, in <module>
            b1.simple_move("worst")
          File "C:/Users/Joshua/PycharmProjects/monarch_simulation/Butterflies.py", line 205, in simple_move
            assert (direction == 'north' or direction == 'south' or direction == 'east' or direction == 'west')
        AssertionError
        >>> b1.position = [50,50]
        >>> b1.simple_move('north')
        >>> print(b1.position)
        [49, 50]
        >>> b1.position = [100,50]
        >>> b1.food_level = 20
        >>> b1.simple_move("North")
        >>> b1
        Monarch with 20.00% food at [99, 50]
        >>> b1.status
        'alive'
        """
        # Ensure a valid ordinal direction was passed into the function
        direction = direction.lower()
        assert (direction == 'north' or direction == 'south' or direction == 'east' or direction == 'west')
        # First check if it exits
        self.check_if_exit()
        if self.status == 'exit':
            return self
        else:
            # if the pollinator is on the border, move randomly
            if self.position[0] == 0 or self.position[0] == self.area_length - 1 or \
                    self.position[1] == 0 or self.position[1] == self.area_width - 1:
                self.random_move()

            # Otherwise it will make a basic moves
            elif direction == 'north':
                self.position[0] -= 1
                self.moves.append(copy.deepcopy(self.position))
                self.decrement_food(self.__class__.__food_unit)

            elif direction == 'south':
                self.position[0] += 1
                self.moves.append(copy.deepcopy(self.position))
                self.decrement_food(self.__class__.__food_unit)

            elif direction == 'east':
                self.position[1] += 1
                self.moves.append(copy.deepcopy(self.position))
                self.decrement_food(self.__class__.__food_unit)

            elif direction == 'west':
                self.position[1] -= 1
                self.moves.append(copy.deepcopy(self.position))
                self.decrement_food(self.__class__.__food_unit)

            else:
                raise ValueError("Direction not recognized")

    def seek_resource(self, resource: str) -> int:
        """
        The pollinator seeks the designated resource
        :param resource: A resource to seek must be declared
        :return: return self sends it back when it is done, otherwise it modifies self and returns self and turns
        taken to complete the operation
        """
        # Let's make sure no zombie pollinators are looking for our resources
        if self.status == 'dead':
            return self, 0

        times = np.random.randint(10)
        if resource == 'shelter':
            if not self.shelter_indices:
                # There's no shelter, so it just wanders :(
                self.random_move(times)
                self.turns += times
                return self, times
            else:
                if tuple(self.position) in self.shelter_indices:
                    nearest = tuple(self.position)
                else:
                    nearest = min(self.shelter_indices, key=lambda x: distance(x, self.position))

        elif resource == 'food':
            if not self.food_indices:
                # There's no food, so it just wanders :(
                self.random_move(times)
                self.turns += times
                return self, times
            else:
                if tuple(self.position) in self.food_indices:
                    nearest = tuple(self.position)
                else:
                    nearest = min(self.food_indices, key=lambda x: distance(x, self.position))

        else:
            raise ValueError('Unknown resource')

        # Record the nearest value
        x = nearest[0]
        y = nearest[1]

        # There's a random chance it can't reach the resource, otherwise it does
        # and spends the appropriate amount of energy to get there

        if np.random.choice([1, 0], p=[0.999, 0.001]):
            old_position = self.position
            self.record_moves(x, y)
            self.decrement_food(distance(old_position, self.position) * self.__class__.__food_unit)
            return self, distance(self.position, nearest)

        # Moves randomly instead of seeking resource. Better luck next time.
        else:
            self.random_move(times)
            self.food_level -= self.__class__.__food_unit * times
            return self, times

    def move_one_day(self):
        """
        The idea here is to simulate one day in the life of a pollinator. For convenience, one loop will represent 25
        seconds of the life of the pollinator, which I sometimes refer to as 1 'turn' because I used to play a lot
        of pen-and-paper rpgs. I'll create class-specific methods to define the actual actions taken, but basically
        I'll divide the day into early morning, late mornning, noonish, early afternoon, late afternoon, and night.
        Because pollinators all rely on flowers, they tend to be most active early and later in the day, preferring to
        shelter when the day is hottest, and all rest at night when the flowers are more or less dormant. This
        should allow me to generalize a day of a pollinator and get more specific in their subclasses. I'll assume a
        day runs from 4am to the next 4am, though a pollinator could jump into this method at any time. Those entering
        later will get a pro-rated day, though the assumption is the wrapper will run the sim until they die or leave,
        so not getting a full day for the first day shouldn't hurt them overall.
        :param hours: current number of seconds
        :param seconds: current hours
        :param days: number of days elapsed. This simulation section is desgined to cover one day and then quit, but
        of course that may not always happen. And a monarch may start on a different day rather than the first day
        of the simulation.
        :return: the Monarch object, appropriately manipulated
        """
        # A false flag. Not in that way.
        flag = False
        while self.status == 'alive':
            temp_days, self.hours, self.seconds = increment_day(self.days, self.hours, self.seconds)
            # Basically, if something weird gets passed in and the increment turns out to add an entire day to the total
            # We'll add the extra number of days onto the days count and just stop Hopefully this will smooth out any
            # weird inputs from the outer layers This should also handle cases where a pollinator moved randomly for a
            # long time looking for a resource
            if temp_days > 0:
                self.days += temp_days
                break

            # Assuming we didn't somehow way overshoot a day (code above), if the flag has been set,
            # then we increment a day and break the loop
            if flag:
                self.days += 1
                break

            # If this is the last iteration of the day, set the flag and increment a day
            if self.hours == 3 and (3600 >= self.seconds >= 3575):
                flag = True


            # Early morning activitny
            if 4 <= self.hours < 6:
                self.morning_activity()
                # make sure it's not a zombie butterfly
                if self.status == 'dead':
                    break

            elif 6 <= self.hours < 12:
                if self.seconds == 0:
                    print("late morning activity")
                self.late_morning_activity()
                # make sure it's not a zombie butterfly
                if self.status == 'dead':
                    break

            elif 12 <= self.hours < 19:
                self.afternoon_activity()
                # make sure it's not a zombie butterfly
                if self.status == 'dead':
                    break

            elif 19 <= self.hours < 21:
                self.late_afternoon_activity()
                # make sure it's not a zombie butterfly
                if self.status == 'dead':
                    break

            elif 21 <= self.hours < 24 or 0 <= self.hours < 4:
                self.night_time_activity()
                # make sure it's not a zombie butterfly
                if self.status == 'dead':
                    break

            else:
                raise ValueError("hours out of range during move")

            # make sure it's not a zombie butterfly
            if self.status == 'dead':
                break

            # now that it has moved, if it's near shelter and not already in shelter
            # there's a chance it may take shelter, assuming it's not too hungry
            if self.food_level >= 25.0:
                if self.area.array[self.position[0]][self.position[1]] == 3 and self.sheltered is False:
                    if np.random.choice([True, False], p=[self.__class__.__shelter_chance, 1-self.__class__.__shelter_chance]):
                        self.sheltered = True

                # slightly less chance of taking shelter in a mixed food/shelter area
                elif self.area.array[self.position[0]][self.position[1]] == 4 and self.sheltered is False:
                    if np.random.choice([True, False], p=[.9 * self.__class__.__shelter_chance, 1-(.9 * self.__class__.__shelter_chance)]):
                        self.sheltered = True

            # if it's near food, it will most likely try to eat
            # There's no class-level variable for this since all pollinators have to eat
            # and actively seek food sources in flowers.
            if self.area.array[self.position[0]][self.position[1]] == 2:
                if np.random.choice([True, False], p=[0.99, 0.01]):
                    self.food_level = 100

            # Less chance of eating in a mixed food/shelter area due to less food availability
            if self.area.array[self.position[0]][self.position[1]] == 4:
                if np.random.choice([True, False], p=[0.80, 0.2]):
                    self.food_level = 100

            # Increment time
            self.seconds += 25 * self.turns
            self.turns = 0

            #check for death
            self.check_for_death()
            if self.status == "dead":
                break

    # As baseline behavior, we'll say a pollinator looks for food all day, then at night seeks shelter
    def morning_activity(self):
        self.seek_resource("food")

    def late_morning_activity(self):
        self.seek_resource("food")

    def afternoon_activity(self):
        self.seek_resource("food")

    def late_afternoon_activity(self):
        self.seek_resource('food')

    def night_time_activity(self):
        self.seek_resource('shelter')

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
    Monarch with 100.00% food at [1, 3]
    """

    __food_unit = 0.0225
    __death_factor = 0.01
    __can_exit_north = True
    __exit_chance = 0.9
    __shelter_chance = 0.01


    def __init__(self, area: CropField):
        Pollinator.__init__(self, area)
        # This gives the starting position
        variable = np.random.choice([0, 1, 2, 3], p=[0.625, 0.125, 0.125, 0.125])
        if variable == 0:
            temp_position = [self.area_length - 1, np.random.randint(self.area_width)]
        elif variable == 1:
            temp_position = [np.random.randint(int(self.area_length / 2)), 0]
        elif variable == 2:
            temp_position = [np.random.randint(int(self.area_length / 2)), self.area_width - 1]
        else:
            if self.shelter_indices:
                temp_position = list(self.shelter_indices[np.random.choice(len(self.shelter_indices))])
            else:
                temp_position = [self.area_length-1, 0]
        self.position = temp_position
        self.moves = [copy.deepcopy(self.position)]

    def morning_activity(self):
        '''
        For the first couple hours in the morning, monarchs will typically seek food.
        '''

        # If it's in shelter during the day light, there's a small chance it will just stay put, unless
        # it is super hungry
        if self.sheltered:
            # number of times it will move randomly
            times = np.random.randint(10)
            # Just a check to make sure it is actually in a tree area and marked as sheltered...
            if self.area.array[self.position[0]][self.position[1]] not in [3, 4]:
                self.sheltered = False
                self.random_move(times)
                # One turn consumes 25 seconds
                self.turns += times
            # if it's still sheltered but it's food level is low, or random chance kicks in, it will leave shelter
            elif self.food_level < 25 or np.random.choice([True, False], p=[0.1, 0.9]):
                self.sheltered = False
                self.random_move(times)
                self.seconds += times
            else:
                # just stay sheltered if those conditions fail
                # Consume half a unit of food
                self.decrement_food(self.__food_unit/2)
                self.turns += 1
        else:
            self, times = self.seek_resource('food')
            # One turn consumes 25 seconds
            self.turns += times

    def late_morning_activity(self):
        # If it's daylight, the priorities will be food if it's hungry and moving north otherwise.
        # It may randomly occasionally seek shelter if it happens to be near a tree.
        # If it's in shelter during the day light, there's a small chance it will just stay put, unless
        # it is super hungry
        # moves possible
        moves_possible = int(self.food_level // self.__food_unit)
        if self.sheltered:
            # number of times it moves randomly
            times = np.random.randint(10)
            # Just a check to make sure it is actually in a tree area and marked as sheltered...
            if self.area.array[self.position[0]][self.position[1]] not in [3, 4]:
                self.sheltered = False
                self.random_move(times)
                self.turns += times

            # If it's still sheltered, meaning its in a legal shelter site, then most likely it will move
            elif self.food_level < 25 or np.random.choice([True, False], p=[.9, .1]):
                self.sheltered = False
                self.random_move(times)
                # One turn consumes 25 seconds
                self.turns += times

            # stay sheltered if those conditions fail
            else:
                self.decrement_food(self.__food_unit / 2)
                self.turns += 1
        else:
            # Above a 50% food level, we'll consider it
            if self.food_level >= 50.0:
                # Usually, it will try to move north

                move_die = np.random.choice(int(moves_possible // 2))

                for i in range(move_die):
                    direction_die = np.random.choice(['north', 'south', 'east', 'west'],
                                                     p=[0.925, 0.025, 0.025, 0.025])
                    random_chance = np.random.choice([0, 1], p=[.995, 0.005])
                    if random_chance:
                        self.random_move()
                    else:
                        self.simple_move(direction_die)

                    self.turns += 1

            # if it's a little hungry, it may seek food
            elif 25.0 <= self.food_level < 50.0:
                if np.random.choice([True, False], p=[0.001, 0.999]):
                    # slight chance of moving randomly instead
                    self.random_move()

                else:
                    # usually look for food
                    self, times = self.seek_resource('food')
                    self.seconds += times
                    return self

            # now it's very hungry and will almost certainly seek food
            elif self.food_level < 25.0:
                if np.random.choice([True, False], p=[0.0001, 0.9999]):
                    self.random_move()

                # otherwise look for food
                else:
                    self, times = self.seek_resource('food')
                    self.seconds = (25*times)
                    return self

    #For the afternoon, it will repeat the late-morning activity
    def afternoon_activity(self):
        if self.seconds == 0:
            print("afternoon activity")
        self.late_morning_activity()
        return self

    # As dusk approaches, it will try to look for food before sheltering for the night.
    # If it's already sheltered, we'll just have it stay sheltered.
    def late_afternoon_activity(self):
        if self.seconds == 0:
            print("late afternoon activity")
        # Number of times to randomly move
        times = np.random.randint(10)
        # If it's still sheltered at this point, break shelter
        if self.sheltered:
            self.sheltered = False
            self.random_move(times)
            self.decrement_food(self.__food_unit)
            self.turns += times
        else:
            # otherwise it's going to look for food to fill its belly before sleep
            self, times = self.seek_resource('food')
            self.turns += times
        return self

    def night_time_activity(self):
        # During the evening, it will prioritize seeking shelter. It will stay in shelter through the night
        # once it locates it, so we'll remove the leave shelter component of the checks. There's no real
        # food to be had at night, so we'll just assume it battens down the hatches. If it's food falls too low
        # it may die. Such is the risk of life.
        if self.seconds == 0:
            print("night time activity")
        # Number of times to randomly move
        times = np.random.randint(10)
        if self.sheltered:
            # At night it will batten down the hatches and stay sheltered
            # If for whatever reason it is marked as sheltered but isn't in a tree...
            if self.area.array[self.position[0]][self.position[1]] not in [3, 4]:
                self.sheltered = False
                self.random_move(times)
                self.turns += times
            else:
                # if it gets here, it's sheltered and in a tree, so just decrement half a food unit
                # and move aling without taking further action
                self.decrement_food(self.__food_unit/2)
                return self
        # This is the case that it is alive and near shelter. At this time it will take shelter
        elif self.area.array[self.position[0]][self.position[1]] in [3, 4]:
            self.sheltered = True
            self.decrement_food(self.__food_unit/2)

        else:
            # otherwise it's going to look for shelter
            self, times = self.seek_resource('shelter')
            self.turns += times
        return self

class Bee(Pollinator):
    '''
    This class will establish some baselines for all types of bees. There are a huge diversity of native and commercial
    bees. The most common bees that people tend to be interested in are the Western honey bee (Apis mellifera) and some
    related species (such as the hybrid 'Africanized honey bee', a cross between A. mellifera and an African
    subspecies), and Bombus impatiens, a domesticated bumble bee. However, there has been a growing interest in native
    bees, such as the wide range of Bombus spp. and solitary bees. Bees generally have a home base, either a nest
    or a hive. Bombus and many solitary bees tend to nest in the ground, while A. mellifera have hives, either in rocky
    areas or trees. We'll try to allow for a diversity of options. Crop fields are generally sprayed with pesticides and
    trampled with farm equipment, so it's less common to find bees nesting in the fields themselves. In general we'll
    consider bees won't wander too far frm their home. Doing so would mean certain death (honey bee and bumble bee
    drones and queens would be the exception, since they leave their nests to start new colonies and breed. I'll focus
    on just the workers and for the general bee I'll assume it can exit, but at a very low chance.
    '''

    __food_unit = .0225
    __death_factor = 0.01
    __can_exit = True
    __exit_chance = 0.1
    __shelter_chance = 0.5


    def __init__(self, area: CropField):
        Pollinator.__init__(self, area)
        self.sheltered = False
        # This gives the position of the nest. I'll assume the nest must be close to either food or shelter
        # One problem most bees have is destruction of their habitat means they won't make nests, so this seems
        # like a logical choice to me
        if area.shelter_indices:
            index = np.random.randint(len(area.shelter_indices))
            self.nest_position = area.shelter_indices[index]

        elif area.food_indices:
            index = np.random.randint(len(area.food_indices))
            self.nest_position = area.food_indices[index]

        # if there's no suitable nest building site, call an error
        else:
            raise ValueError("There is no suitable nesting site for bees. Ensure field has some food or shelter")

        # Initialize the bee's position to its nest.
        self.position = self.nest_position
        self.moves.append(copy.deepcopy(self.position))

    def morning_activity(self):
        '''
        For the first couple hours in the morning, bees will typically seek food.
        :return: self

        # TODO revise and check on bee behavior in general
        '''

        # If it's in shelter during the day light, there's a small chance it will just stay put, unless
        # it is super hungry
        if self.sheltered:
            # Number of times to randomly move
            times = np.random.randint(10)

            # Just a check to make sure it is actually in a tree area and marked as sheltered...
            if self.area.array[self.position[0]][self.position[1]] not in [3, 4]:
                self.sheltered = False
                self.random_move(times)
                self.turns += times
            if self.sheltered and (self.food_level < 25 or np.random.choice([True, False], p=[1 - self.__shelter_chance,
                                                                                              self.__shelter_chance])):
                self.sheltered = False
                self.random_move(times)
                self.turns += times
            else:
                # just stay sheltered if those conditions fail
                # Consume half a unit of food
                self.decrement_food(self.__food_unit / 2)
                # One turn consumes 25 seconds
                self.turns += 1
        else:
            self, times = self.seek_resource('food')
            # One turn consumes 25 seconds
            self.turns += times

    def late_morning_activity(self):
        # If it's daylight, the priorities will be food if it's hungry and moving north otherwise.
        # It may randomly occasionally seek shelter if it happens to be near a tree.
        # If it's in shelter during the day light, there's a small chance it will just stay put, unless
        # it is super hungry
        # moves possible
        moves_possible = int(self.food_level // self.__food_unit)
        if self.sheltered:
            # Number of times to randomly move
            times = np.random.randint(10)

            # Just a check to make sure it is actually in a tree area and marked as sheltered...
            if self.area.array[self.position[0]][self.position[1]] not in [3, 4]:
                self.sheltered = False
                self.random_move(times)
                self.turns += times

            # If it's still sheltered, meaning its in a legal shelter site, then most likely it will move
            if self.sheltered and (self.food_level < 25 or np.random.choice([True, False], p=[1 - self.__shelter_chance,
                                                                                              self.__shelter_chance])):
                self.sheltered = False
                self.random_move(times)
                self.turns += times

            else:
                self.decrement_food(self.__food_unit / 2)
                self.turns += 1
        else:
            # Above a 50% food level, we'll consider it
            if self.food_level >= 50.0:
                # Usually, it will try to move north
                direction_die = np.random.choice(['north', 'south', 'east', 'west'],
                                                 p=[0.925, 0.025, 0.025, 0.025])
                move_die = np.random.choice(int(moves_possible // 2))

                for i in range(move_die):
                    random_chance = np.random.choice([0, 1], p=[.995, 0.005])
                    if random_chance:
                        self.random_move()
                    else:
                        self.simple_move(direction_die)

                    # Each move takse 25 seconds
                    self.turns += 1

            # if it's a little hungry, it may seek food
            elif 25.0 <= self.food_level < 50.0:
                if np.random.choice([True, False], p=[0.001, 0.999]):
                    times = np.random.randint(10)
                    # slight chance of moving randomly instead
                    self.random_move(times)
                    self.turns += times

                else:
                    # usually look for food
                    self, times = self.seek_resource('food')
                    self.turns += times

            # now it's very hungry and will almost certainly seek food
            elif self.food_level < 25.0:
                if np.random.choice([True, False], p=[0.0001, 0.9999]):
                    times = np.random.rantint(10)
                    self.random_move(times)
                    self.turns += times

                # otherwise look for food
                else:
                    self, times = self.seek_resource('food')
                    self.turns = times
                    return self

    # For the afternoon, it will repeat the late-morning activity
    def afternoon_activity(self):
        self.late_morning_activity()

    # As dusk approaches, it will try to look for food before sheltering for the night.
    # If it's already sheltered, we'll just have it stay sheltered.
    def late_afternoon_activity(self):
        # moves possible

        # If it's still sheltered at this point, break shelter
        if self.sheltered:
            # Number of times to randomly move
            times = np.random.randint(10)
            self.sheltered = False
            self.random_move(times)
            self.decrement_food(self.__food_unit * times)
            # Each move takes 25 seconds
            self.turns += times
        else:
            # otherwise it's going to look for food to fill its belly before sleep
            self, times = self.seek_resource('food')
            self.turns += times

    def night_time_activity(self):
        # During the evening, it will prioritize seeking shelter. It will stay in shelter through the night
        # once it locates it, so we'll remove the leave shelter component of the checks. There's no real
        # food to be had at night, so we'll just assume it battens down the hatches. If it's food falls too low
        # it may die. Such is the risk of life.
        if self.sheltered:
            # At night it will batten down the hatches and stay sheltered
            # If for whatever reason it is marked as sheltered but isn't in a tree...
            # Number of times to randomly move
            times = np.random.randint(10)
            if self.area.array[self.position[0]][self.position[1]] not in [3, 4]:
                self.sheltered = False
                self.random_move(times)
                self.turns += times
            else:
                # if it gets here, it's sheltered and in a tree, so just decrement half a food unit
                # and move aling without taking further action
                self.decrement_food(self.__food_unit / 2)
                self.turns += 1
                return self
        # This is the case that it is alive and near shelter. At this time it will take shelter
        elif self.sheltered is False and self.area.array[self.position[0]][self.position[1]] in [3, 4]:
            self.sheltered = True
            self.decrement_food(self.__food_unit / 2)
            self.turns += 1

        else:
            # otherwise it's going to look for shelter
            self, times = self.seek_resource('shelter')
            self.turns += times

def distance(x: list, y: tuple) -> int:
    '''
    This is simply the Manhattan distance, which makes the most sense since our areas are just basically squares and
    pollinators can only move in an ordinal diretion. For this application, these should  be integers, in order
    to give a proper integer answer, though in true manhattan distance this doesn't have to be the case, necessarily.
    As such, I will assert that they are integers just to be complete
    :param x: the current position in the form of a list
    :param y: the current position in the form of a tuple, The only reason this is a tuple and not a list is because
    that's how I set it up in the indices list in the pollinator's class. This would work perfectly fine as a list
    too, since the only thing returned is an integer.
    :return: an integer giving the manhattan distance. Since these are square areas basically it's the number of
    'moves' it takes to get from point x to point y.
    >>> distance([5, 0], (-1, 3))
    9
    '''
    # assert type(x[0]) is int and type(x[1]) is int and type(y[0]) is int and type(y[1]) is int
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def increment_day(days: int, hrs: int, secs: int) -> (int, int, int):
    '''
    This takes seconds and hours and increments it according to a 24-hour clock. Although this theoretically
    shouldn't arise in this calculation, I want to account for if an unusually large number of seconds gets
    passed in, perhaps due to pollinator wandering, and increment the day as well as the time
    :param days: number of days elapsed
    :param hrs: integer number of hours, from 0-23.
    :param secs: arbitrary number of integer seconds. For every 3600 seconds, it will add an hour.
    :return: returns the new value for hours and seconds
    >>> increment_day(5, 87273)
    (1, 5, 873)
    '''
    while secs >= 3600:
        hrs += 1
        secs -=3600  # reduce seconds by 3600 and add an hour
        # at midnight the 24-clock cycles back around to 0
        if hrs == 24:
            hrs = 0
            days += 1
    return days, hrs, secs


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
    base_field_base_rows = [4] * 100
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
        while monarch1.status == "alive":
            monarch1.move_one_day()
        results.append(monarch1.status)
    dictionary["test_field_{}".format(number)] = [100 * results.count('dead') / len(results)]
    print("Dead percentage = {:.2f}%".format(100 * results.count('dead') / len(results)))
    print("Exit percentage = {:.2f}%".format(100 * results.count('exit') / len(results)))
    print("--- %s seconds ---" % (time.time() - start_time))
    return dictionary


def iterate_field(group: list, type: str = None) -> CropField:
    """
    Iterate groups of fields to find optimal arrangements.

    :param group: The field group to be optimized
    :param type: What to optimize (food, shelter, or none).
    :return: Optimal cropfield
    TODO: modify this code
    """
    field = group[0]
    food_index = np.where(field.array == 2)  # get locations of food in field
    shelter_indices = np.where(field.array == 3)  # get locations of shelter in field
    food_ix_ix = len(food_index[0])  # indices of the food indices
    shelter_ix_ix = len(shelter_indices[0])  # indices of the shelter indices
    max_len = len(field.array)
    max_width = len(field.array[0])
    iterated_field = field
    # This gets complicated, but I'm picking a random amount of food indices to randomly move
    if type is None or type == 'Both':
        food_sites_to_iterate = np.random.choice(food_ix_ix,
                                                 np.random.randint(food_ix_ix),
                                                 replace=False)  # choose a random number of food sites to move
        food_sites_to_iterate.sort()
        shelter_sites_to_iterate = np.random.choice(shelter_ix_ix,
                                                    np.random.randint(shelter_ix_ix),
                                                    replace=False)  # same but for shelter
        shelter_sites_to_iterate.sort()
    elif type == 'Death':
        food_sites_to_iterate = np.random.choice(food_ix_ix,
                                                 np.random.randint(food_ix_ix / np.random.randint(1, 11)),
                                                 replace=False)  # choose a random number of food sites to move
        food_sites_to_iterate.sort()
        shelter_sites_to_iterate = np.random.choice(shelter_ix_ix,
                                                    np.random.randint(shelter_ix_ix),
                                                    replace=False)  # same but for shelter
        shelter_sites_to_iterate.sort()
    else:
        food_sites_to_iterate = np.random.choice(food_ix_ix,
                                                 np.random.randint(food_ix_ix),
                                                 replace=False)  # choose a random number of food sites to move
        food_sites_to_iterate.sort()
        shelter_sites_to_iterate = np.random.choice(shelter_ix_ix,
                                                    np.random.randint(shelter_ix_ix / np.random.randint(1, 11)),
                                                    replace=False)  # same but for shelter
        shelter_sites_to_iterate.sort()
    for food in food_sites_to_iterate:
        # This if statement and the one below is my attempt to group together similar items. I feel
        # that is more realistic in a managed field. Certainly the results I was getting before
        # doing this were valid, but an equally distributed field of crops, food and shelter is probably
        # not viable at this time. Dropping these if statements will give fields with more uniform
        # distribution.
        try:
            if abs(food_index[0][food] - food_index[0][food+1]) <= 1 or \
                    abs(food_index[0][food] - food_index[0][food-1]) <= 1 or \
                    abs(food_index[1][food] - food_index[1][food+1]) <= 1 or \
                    abs(food_index[1][food] - food_index[1][food-1]) <= 1:
                pass
        except IndexError:
            pass
        else:
            random_x = np.random.randint(max(food_index[0][food] - np.random.randint(0.1*max_len), 0),
                                         min(food_index[0][food] + np.random.randint(0.1*max_len) + 1, max_len))
            random_y = np.random.randint(max(food_index[1][food] - np.random.randint(0.1*max_width), 0),
                                         min(food_index[1][food] + np.random.randint(0.1*max_width) + 1, max_width))
            iterated_field.array[food_index[0][food]][food_index[1][food]] = 1
            iterated_field.array[random_x][random_y] = 2
    for shelter in shelter_sites_to_iterate:
        try:
            if abs(shelter_indices[0][shelter] - shelter_indices[0][shelter+1]) <= 1 or \
                    abs(shelter_indices[0][shelter] - shelter_indices[0][shelter-1]) <= 1 or \
                    abs(shelter_indices[1][shelter] - shelter_indices[1][shelter+1]) <= 1 or \
                    abs(shelter_indices[1][shelter] - shelter_indices[1][shelter-1]) <= 1:
                pass
        except IndexError:
            pass
        else:
            random_x = np.random.randint(max(shelter_indices[0][shelter] - np.random.randint(0.1*max_len), 0),
                                         min(shelter_indices[0][shelter] + np.random.randint(0.1*max_len) + 1, max_len))
            random_y = np.random.randint(max(shelter_indices[1][shelter] - np.random.randint(0.1*max_width), 0),
                                         min(shelter_indices[1][shelter] + np.random.randint(0.1*max_width) + 1, max_width))
            iterated_field.array[shelter_indices[0][shelter]][shelter_indices[1][shelter]] = 1
            iterated_field.array[random_x][random_y] = 3
    return iterated_field


def optimize_field(field: CropField, rows: int = 4, columns: int = 4, dead_goal: int = 100, exit_goal: int = 0,
                   num_iters: int = 25, total_iters: int = math.inf) -> CropField:
    '''
    The goal of this function is to find an optimal arrangement of fields. It will start with a single field and repeat
    it across several rows and columns, then run butterflies through the entire set and see if we can find an optimal
    arrangement of fields. For example, maybe a fallow field in the middle is best, or maybe if there are food borders
    around each field works best.
    :param field:
    :param rows:
    :param columns:
    :param dead_goal:
    :param exit_goal:
    :param num_iters:
    :param total_iters:
    :return:
    '''
    # Simulate to see how well the field does
    pass


def graphic_display (field: Area, array: np.array) -> None:
    """
    This will take a field and an array defining the path the pollinator took and turn it into a heatmap

    :param field: an area the pollinator lives on which it spent it's simulated time on
    :param array: a collection of moves made by the pollinator.
    :return: No return, it simply displays a plot.
    """
    pass

def basic_test (field: Area, iterations: int) -> None:
    starttime = time.time()
    results = []
    for k in range(iterations):
        monarch = Monarch(field)
        monarch.move_one_day()
        results.append([copy.deepcopy(monarch.status), copy.deepcopy(monarch.cause_of_death),
                        copy.deepcopy(monarch.moves)])

    # basic results
    print(results)
    dead_count = 0
    exit_count = 0
    alive_count = 0
    for temp in results:
        dead_count += temp.count('dead')
        exit_count += temp.count('exit')
        alive_count += temp.count('alive')
    print("Dead percentage = {:.2f}%".format(100 * dead_count / len(results)))
    print("Exit percentage = {:.2f}%".format(100 * exit_count / len(results)))
    print("Alive percentage = {:.2f}%".format(100 * alive_count / len(results)))
    print("--- %s seconds ---" % (time.time() - starttime))

    results = pd.DataFrame(results)
    print(results[2][0])
    #save details for further manipulation
    newfile = 'monarch_results.pk'
    with open(newfile, 'wb') as fi:
        pickle.dump(results, fi)


def main():
    # # this is the optimization simulation. Start with a random field and try to optimize it
    # testfield = CropField.random_field(3400, 100, 90, 5, 5)
    # print(testfield.row_len * 15, testfield.col_len * 15)
    # print('starting test')
    # b1 = Monarch(testfield)
    # print (b1)
    # bee1 = Bee(testfield)
    # print(bee1)
    # b1.move_one_day()
    # print(bee1.moves)



    # This is the basic simulation, run a bunch of single butterflies over the course of the day and see how they fare
    testfield = CropField(np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [2, 2, 2, 2]]))
    basic_test(testfield, 1000)
    # for i in range(10):
    #     b1 = Monarch(testfield)
    #     print(b1)
    # print(b1.moves)
    # b1.record_moves(2, 2)
    # print(b1)
    # print(b1.moves)
    # b1.random_move()
    # print(b1)
    # print(b1.moves)

    # # first analysis
    # master_results = {}
    # for i in range(0, 8):
    #     test_field(master_results, i)
    # index = ['standard', 'food_heavy', 'middle_food', 'middle_shelter', 'shelter_heavy', 'balanced_random',
    #          'food_random', 'shelter_random']
    # master_results = pd.DataFrame(master_results).T
    # # print(master_results)
    # master_results.index = index
    # print("The best-performing field was {}".format(master_results[0].idxmin()))


if __name__ == '__main__':
    main()

    # field stats
    # field = create_middle_shelter_windbreak_test(333)
    # food = len(field[field == 2].stack().index.tolist())
    # shelter = len(field[field == 3].stack().index.tolist())
    # crops = len(field[field == 1].stack().index.tolist())
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
    # food = len(field_test[field_test == 2].stack().index.tolist())
    # shelter = len(field_test[field_test == 3].stack().index.tolist())
    # crops = len(field_test[field_test == 1].stack().index.tolist())
    # total = food + shelter + crops
    # print('Percent food: {:.2f}%'.format(math.ceil(100 * food/total)))
    # print("Percent shelter: {:.2f}%".format(math.ceil(100 * shelter/total)))
    # print("Percent crops: {:.2f}%".format(math.floor(100 * crops/total)))
