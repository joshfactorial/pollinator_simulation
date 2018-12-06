#!/home/joshua/anaconda3/bin/python

import copy
from Functions import distance
from Area import *


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

    def food_unit(self):
        return self.__class__.__food_unit

    def death_factor(self):
        return self.__death_factor

    def exit_chance(self):
        return self.__exit_chance

    def can_exit_north(self):
        return self.__can_exit_north

    def can_exit(self):
        return self.__can_exit

    def shelter_chance(self):
        return self.__shelter_chance

    def kill_it(self):
        self.status = 'dead'
        return

    def check_for_death(self):
        # Based on how much food it currently has, the Monarch's chances to die randomly change.
        roll_die = np.random.random_sample()
        if self.food_level > 90 and roll_die < self.__death_factor / 1000:
            self.kill_it()
            return
        elif 50.0 < self.food_level <= 90 and roll_die < self.__death_factor / 100:
            self.kill_it()
            return
        elif 25.0 < self.food_level <= 50.0 and roll_die <= self.__death_factor:
            self.kill_it()
            return
        elif 0.01 <= self.food_level <= 25.0 and roll_die < self.__death_factor * 50:
            self.kill_it()
            return
        elif self.food_level < 0.01 and roll_die < self.__death_factor * 99:
            self.status == 'dead'
            return
        else:
            return

    def decrement_food(self, amount):
        if self.food_level >= amount:
            self.food_level -= amount
        else:
            self.food_level = 0
        return

    def check_if_exit(self):
        """
        This function checks to see if a Pollinator is on an exit boundary and if so, if it can exit, and if so whether
        it does or not. Some of this code repeats with code in other places and could probably be refactored into
        a new class or function.
        :return: None
        testfield =
        """
        # Case 1: it can exit or exit north and is in the top row.
        if (self.__can_exit_north or self.__can_exit) and self.position[0] == 0:
            self.status = np.random.choice(['exit', 'alive'],
                                           p=[self.__exit_chance, 1 - self.__exit_chance])
        # Case 2: It can exit and is on the bottom row, the left column or the right column
        elif self.__can_exit and (self.position[0] == self.area_length - 1 or
                                            self.position[1] == 0 or self.position[1] == self.area_width - 1):
            self.status = np.random.choice(['exit', 'alive'],
                                           p=[self.__exit_chance, 1 - self.__exit_chance])
        # Case 3: It is outside the borders.
        elif (self.position[0] < 0 or self.position[0] > self.area_length - 1 or
              self.position[1] < 0 or self.position[1] > self.area_width - 1):
            # If it CAN exit and it's wandered off the map, just mark it as gone
            if self.__can_exit or self.__can_exit_north:
                self.status = 'exit'
            # It CAN'T exit and needs to be returned to the map. We'll look through the moves list and find a time
            # when it was on the map, then return it to that position. All Pollinators start on the map, so this will
            # always find at least one valid index.
            for i in range(len(self.moves)):
                if self.area_length-1 >= self.moves[-i][0] >=0 and self.area_width-1 >= self.moves[-i][1] >= 0:
                    self.position = self.moves[-i]

    def record_moves(self, x1, y1):
        x0 = copy.deepcopy(self.position[0])
        y0 = copy.deepcopy(self.position[1])
        if x0 == x1 and y0 == y1:
            self.turns += 1
            self.moves.append([x0, y0])
        if x1 > x0:
            for i in range(abs(x0 - x1)):
                x0 += 1
                self.moves.append([x0, y0])
                self.turns += 1
        elif x1 < x0:
            for i in range(abs(x0 - x1)):
                x0 -= 1
                self.moves.append([x0, y0])
                self.turns += 1
        else:
            pass
        if y1 > y0:
            for j in range(abs(y0 - y1)):
                self.position[1] += 1
                self.moves.append([x0, y0])
                self.turns += 1
        elif y1 < y0:
            for i in range(abs(y0 - y1)):
                self.position[1] -= 1
                self.moves.append([x0, y0])
                self.turns += 1
        else:
            pass

    def random_move(self, number: int = 1):
        # Standard random move
        for i in range(number):
            # If it's on the border, check to see if it can exit
            if (self.__can_exit or self.__can_exit_north) and (self.position[0] in [self.area_length - 1, 0]
                                                               or self.position[1] in [self.area_width - 1, 0]):
                self.turns += 1
                self.decrement_food(self.food_unit)
                self.check_if_exit()
                if self.status == 'exit':
                    return
                else:
                    if self.position[0] - 1 >= 0:
                        self.position[0] -= 1
                    elif self.position[1] - 1 >= 0:
                        self.position[1] -= 1
                    elif self.position[1] + 1 <= self.area_width - 1:
                        self.position[1] += 1
                    elif self.position[0] + 1 <= self.area_length - 1:
                        self.position[0] += 1
                    else:
                        raise ValueError("no idea where this butterfly is")
            # If it's on the border and can't exit, then this will make sure it makes some move
            elif self.position[0] in [self.area_length - 1, 0] or self.position[1] in [self.area_width - 1, 0]:
                self.turns += 1
                self.decrement_food(self.__food_unit)
                if self.position[0] - 1 >= 0:
                    self.position[0] -= 1
                elif self.position[1] - 1 >= 0:
                    self.position[1] -= 1
                elif self.position[1] + 1 <= self.area_width - 1:
                    self.position[1] += 1
                elif self.position[0] + 1 <= self.area_length - 1:
                    self.position[0] += 1
                else:
                    raise ValueError("no idea where this butterfly is")
            # Not on the border, so we use a random move generator
            else:
                coord = np.random.choice((0, 1))
                direction = np.random.choice((-1, 1))
                if coord == 0:
                    # Move north-south
                    if self.area_length - 1 > self.position[0] > 0:
                        self.position[coord] += direction
                        self.decrement_food(self.__food_unit)
                        self.moves.append(copy.deepcopy(self.position))
                    else:
                        raise ValueError("Somehow it is on the border but didn't get "
                                         "the border check and tried to move.")
                else:
                    # Move east-west
                    if self.area_width - 1 > self.position[1] > 0:
                        self.position[1] += direction
                        self.decrement_food(self.__food_unit)
                        self.moves.append(copy.deepcopy(self.position))
                    else:
                        raise ValueError("Somehow it is on the border but didn't get "
                                         "the border check and tried to move.")

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
          File "C:/Users/Joshua/PycharmProjects/pollinator_simulation/Butterflies.py", line 205, in simple_move
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
            return
        else:
            # if the pollinator is on the border, move randomly
            if self.position[0] == 0 or self.position[0] == self.area_length - 1 or \
                    self.position[1] == 0 or self.position[1] == self.area_width - 1:
                self.random_move()

            # Otherwise it will make a basic moves
            elif direction == 'north':
                self.position[0] -= 1
                self.moves.append(copy.deepcopy(self.position))
                self.decrement_food(self.__food_unit)

            elif direction == 'south':
                self.position[0] += 1
                self.moves.append(copy.deepcopy(self.position))
                self.decrement_food(self.__food_unit)

            elif direction == 'east':
                self.position[1] += 1
                self.moves.append(copy.deepcopy(self.position))
                self.decrement_food(self.__food_unit)

            elif direction == 'west':
                self.position[1] -= 1
                self.moves.append(copy.deepcopy(self.position))
                self.decrement_food(self.__food_unit)

            else:
                raise ValueError("Direction not recognized")

    def seek_resource(self, resource: str) -> int:
        """
        The pollinator seeks the designated resource
        :param resource: A resource to seek must be declared
        :return: return sends it back when it is done, otherwise it modifies self and returns self and turns
        taken to complete the operation
        >>> f = CropField([[1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1]])
        >>> b1 = Monarch(f)
        >>> b1.food_level = 100
        >>> b1.position = [1, 3]
        """
        # Let's make sure no zombie pollinators are looking for our resources
        if self.status == 'dead':
            return

        times = np.random.randint(1, 11)
        if resource == 'shelter':
            if not self.shelter_indices:
                # There's no shelter, so it just wanders :(
                self.random_move(times)
                self.turns += times
                return
            else:
                if tuple(self.position) in self.shelter_indices:
                    # In order to prevent a Butterfly from lingering on a food or shelter square
                    # too long, I'm introducing a 50-50 chance that it moves randomly if it's
                    # already on a square containing what it wants.
                    if np.random.choice([1, 0]):
                        nearest = tuple(self.position)
                        # To ensure that at least one time unit is consumed if it doesn't move
                        self.turns += 1
                    else:
                        self.random_move(times)
                        self.turns += times
                        return
                else:
                    nearest = min(self.shelter_indices, key=lambda x: distance(x, self.position))

        elif resource == 'food':
            if not self.food_indices:
                # There's no food, so it just wanders :(
                self.random_move(times)
                self.turns += times
                return
            else:

                if tuple(self.position) in self.food_indices:
                    # Same as seeking shelter above
                    if np.random.choice([1, 0]):
                        nearest = tuple(copy.deepcopy(self.position))
                        self.turns += 1
                    else:
                        self.random_move(times)
                        self.turns += times
                        return
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
            self.record_moves(x, y)
            self.position = [x, y]
            self.decrement_food(self.turns * self.__food_unit)
            return

        # Moves randomly instead of seeking resource. Better luck next time.
        else:
            self.random_move(times)
            self.food_level -= self.__food_unit * times
            self.turns += times
            return

    def increment_time(self):
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
        while self.seconds >= 3600:
            self.hours += 1
            self.seconds -= 3600  # reduce seconds by 3600 and add an hour
            # at midnight the 24-clock cycles back around to 0
            if self.hours == 24:
                self.hours = 0
                self.days += 1

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
        temp_days = self.days
        while self.status == 'alive':
            self.increment_time()
            # Basically, if something weird gets passed in and the increment turns out to add an entire day to the total
            # We'll add the extra number of days onto the days count and just stop Hopefully this will smooth out any
            # weird inputs from the outer layers This should also handle cases where a pollinator moved randomly for a
            # long time looking for a resource
            if self.days > temp_days:
                break

            # Assuming we didn't somehow way overshoot a day (code above), if the flag has been set,
            # then we increment a day and break the loop
            if flag:
                self.days += 1
                break

            # If this is the last iteration of the day, set the flag and increment a day
            if self.hours == 3 and (3600 >= self.seconds >= 3575):
                flag = True

            # Early morning activity
            if 4 <= self.hours < 6:
                self.morning_activity()
                # make sure it's not a zombie butterfly
                if self.status == 'dead':
                    break

            elif 6 <= self.hours < 12:
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
                    if np.random.choice([True, False],
                                        p=[self.__shelter_chance, 1 - self.__shelter_chance]):
                        self.sheltered = True

                # slightly less chance of taking shelter in a mixed food/shelter area
                elif self.area.array[self.position[0]][self.position[1]] == 4 and self.sheltered is False:
                    if np.random.choice([True, False], p=[.9 * self.__shelter_chance,
                                                          1 - (.9 * self.__shelter_chance)]):
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

            # check for death
            self.check_for_death()
            self.check_if_exit()
            if self.status == 'dead' or self.status == 'exit':
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
        super(Monarch, self).__init__()
        # This gives the starting position
        variable = np.random.choice([0, 1, 2, 3], p=[0.625, 0.125, 0.125, 0.125])
        if variable == 0:
            temp_position = [self.area_length - 1, np.random.randint(self.area_width)]
        elif variable == 1:
            temp_position = [np.random.randint(int(self.area_length/2), self.area_length-1), 0]
        elif variable == 2:
            temp_position = [np.random.randint(int(self.area_length/2), self.area_length-1), self.area_width-1]
        else:
            if self.shelter_indices:
                temp_position = list(self.shelter_indices[np.random.choice(len(self.shelter_indices))])
            else:
                temp_position = [self.area_length - 1, 0]
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
                self.decrement_food(self.__food_unit / 2)
                self.turns += 1
        else:
            self.seek_resource('food')

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
                    self.seek_resource('food')
                    return

            # now it's very hungry and will almost certainly seek food
            elif self.food_level < 25.0:
                if np.random.choice([True, False], p=[0.0001, 0.9999]):
                    self.random_move()

                # otherwise look for food
                else:
                    self.seek_resource('food')
                    return

    # For the afternoon, it will repeat the late-morning activity
    def afternoon_activity(self):
        self.late_morning_activity()
        return

    # As dusk approaches, it will try to look for food before sheltering for the night.
    # If it's already sheltered, we'll just have it stay sheltered.
    def late_afternoon_activity(self):
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
            self.seek_resource('food')
        return

    def night_time_activity(self):
        # During the evening, it will prioritize seeking shelter. It will stay in shelter through the night
        # once it locates it, so we'll remove the leave shelter component of the checks. There's no real
        # food to be had at night, so we'll just assume it battens down the hatches. If it's food falls too low
        # it may die. Such is the risk of life.

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
                self.decrement_food(self.__food_unit / 2)
                return
        # This is the case that it is alive and near shelter. At this time it will take shelter
        elif self.area.array[self.position[0]][self.position[1]] in [3, 4]:
            self.sheltered = True
            self.decrement_food(self.__food_unit / 2)

        else:
            # otherwise it's going to look for shelter
            self.seek_resource('shelter')
        return


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
        self.moves = []
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
            self.seek_resource('food')

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
                    self.seek_resource('food')

            # now it's very hungry and will almost certainly seek food
            elif self.food_level < 25.0:
                if np.random.choice([True, False], p=[0.0001, 0.9999]):
                    times = np.random.rantint(10)
                    self.random_move(times)
                    self.turns += times

                # otherwise look for food
                else:
                    self.seek_resource('food')
                    return

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
            self.seek_resource('food')

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
                return
        # This is the case that it is alive and near shelter. At this time it will take shelter
        elif self.sheltered is False and self.area.array[self.position[0]][self.position[1]] in [3, 4]:
            self.sheltered = True
            self.decrement_food(self.__food_unit / 2)
            self.turns += 1

        else:
            # otherwise it's going to look for shelter
            self.seek_resource('shelter')