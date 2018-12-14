#!/home/joshua/anaconda3/bin/python

from Land_Use.Land import Area
from Functions.Operations import manhattan_distance
import numpy as np


class Pollinator:
    """
    Generic Pollinator class which the others will be based on. All animals are tied to an Land_Use, so there must be an

    >>> b1 = Pollinator()
    >>> b1.food_level = 50
    >>> print(b1)
    Pollinator with 50.0% food at (0, 0), status: alive
    >>> b1
    Pollinator: 50.0% food at (0, 0), status: alive
    """

    food_unit = 0.5
    death_factor = 0.5
    exit_chance = 0
    # Some pollinator_types will try to exit if they are near the edge
    can_exit_north = False
    # Others will only exit if on the north edge (e.g., monarchs)
    can_exit = False
    shelter_chance = 0.5

    def __init__(self, area: Area = Area([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [4, 4, 4, 4]]),
                 days: int = 0, hours: int = 4, seconds: int = 0, position: tuple = (0, 0)):
        """
        This class is dependent on the Area class, as a pollinator must exist somewhere in this simulation. So the input
        is an Area, and it performs some calculations to
        :param area: An area object, default is a simple 4x4 area
        """
        # Pollinators start out alive with a random amount of food from a normal distribution centered at 50.
        self.food_level = float(int(np.random.normal(50, scale=20)))
        if self.food_level < 0.0:
            self.food_level = 0.0
        elif self.food_level > 100.0:
            self.food_level = 100.0
        self.status = "alive"
        self.area_length = area.shape[0]
        self.area_width = area.shape[1]
        self.area = area
        self.position = position
        self.moves = [position]
        self.sheltered = False
        self.food_indices = area.food_indices
        self.shelter_indices = area.shelter_indices
        # This defines the starting time of the pollinator. For the simualtion, the inital time will start a 4 am,
        # which is roughly sunup in the midwest in the summer. But other pollinator_types that enter may enter at different
        # times, so I'll leave it open.
        self.days = days
        self.hours = hours
        self.seconds = seconds
        self.turns = 0

    def __str__(self):
        return '{} with {:.1f}% food at {}, status: {}'.format(type(self).__name__, self.food_level, self.position,
                                                               self.status)

    def __repr__(self):
        return '{}: {:.1f}% food at {}, status: {}'.format(type(self).__name__, self.food_level, self.position,
                                                               self.status)

    def kill_it(self):
        """
        Right now this is a simple function to set the pollinator's status to "dead." I may improve this in the future
        :return: None | self
        """
        self.status = 'dead'

    def check_for_death(self):
        """
        Based on how much food it currently has, the pollinator's chances to die randomly change.
        :return: None | self
        """
        roll_die = np.random.random_sample()
        if self.food_level > 90 and roll_die < self.death_factor / 1000:
            self.kill_it()
            return
        elif 50.0 < self.food_level <= 90 and roll_die < self.death_factor / 100:
            self.kill_it()
            return
        elif 25.0 < self.food_level <= 50.0 and roll_die <= self.death_factor:
            self.kill_it()
            return
        elif 0.01 <= self.food_level <= 25.0 and roll_die < self.death_factor * 50:
            self.kill_it()
            return
        elif self.food_level < 0.01 and roll_die < self.death_factor * 99:
            self.status == 'dead'
            return
        else:
            return

    def decrement_food(self, amount):
        """
        This is a simple setting of food level, the only wrinkle is that it makes sure the level doesn't drop
        below zero
        :param amount: amount to decrement the food level
        :return: None | self
        >>> b1 = Pollinator()
        >>> b1.food_level = 50.0
        >>> b1.decrement_food(10)
        >>> b1
        Pollinator: 40.0% food at (0, 0), status: alive
        >>> b1.food_level = 50
        >>> b1.decrement_food(10)
        >>> b1
        Pollinator: 40.0% food at (0, 0), status: alive
        >>> b1.food_level = 50
        >>> b1.decrement_food(10.2)
        >>> b1
        Pollinator: 39.8% food at (0, 0), status: alive
        """
        if self.food_level >= amount:
            self.food_level -= amount
        else:
            self.food_level = 0

    def check_if_exit(self):
        """
        This function checks to see if a Pollinator is on an exit boundary and if so, if it can exit, and if so whether
        it does or not. Some of this code repeats with code in other places and could probably be refactored into
        a new class or function. There is a degree of randomness built into this function
        :return: None

        """
        # Case 1: it can exit or exit north and is in the top row.
        if (self.can_exit_north or self.can_exit) and self.position[0] == 0:
            self.status = np.random.choice(['exit', 'alive'],
                                           p=[self.exit_chance, 1 - self.exit_chance])
        # Case 2: It can exit and is on the bottom row, the left column or the right column
        elif self.can_exit and (self.position[0] == self.area_length - 1 or
                                            self.position[1] == 0 or self.position[1] == self.area_width - 1):
            self.status = np.random.choice(['exit', 'alive'],
                                           p=[self.exit_chance, 1 - self.exit_chance])
        # Case 3: It is outside the borders.
        elif (self.position[0] < 0 or self.position[0] > self.area_length - 1 or
              self.position[1] < 0 or self.position[1] > self.area_width - 1):
            # If it CAN exit and it's wandered off the map, just mark it as gone
            if self.can_exit or self.can_exit_north:
                self.status = 'exit'
            # It CAN'T exit and needs to be returned to the map. We'll look through the moves list and find a time
            # when it was on the map, then return it to that position. All Pollinators start on the map, so this will
            # always find at least one valid index.
            for i in range(len(self.moves)):
                if self.area_length-1 >= self.moves[-i][0] >=0 and self.area_width-1 >= self.moves[-i][1] >= 0:
                    self.position = self.moves[-i]

    def record_moves(self, x1: int, y1: int):
        """
        This function takes in a new position and records the moves needed to get from the animal's current
        position to the new position
        :param x1: an integer index for the new x position
        :param y1: an integer index for the new y position[[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]]
        :return: None | self
        >>> b1 = Pollinator()
        >>> b1.food_level = 20
        >>> b1.record_moves(2, 2)
        >>> b1.moves #doctest: +NORMALIZE_WHITESPACE
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        >>> b1.position = (2, 2)
        >>> b1
        Pollinator: 20.0% food at (2, 2), status: alive
        >>> b1.record_moves(2, 2)
        >>> b1.moves
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 2)]
        """
        x0 = self.position[0]
        y0 = self.position[1]
        if x0 == x1 and y0 == y1:
            self.turns += 1
            self.moves.append((x0, y0))
        if x1 > x0:
            for i in range(abs(x0 - x1)):
                x0 += 1
                self.moves.append((x0, y0))
                self.turns += 1
        elif x1 < x0:
            for i in range(abs(x0 - x1)):
                x0 -= 1
                self.moves.append((x0, y0))
                self.turns += 1
        else:
            pass
        if y1 > y0:
            for j in range(abs(y0 - y1)):
                y0 += 1
                self.moves.append((x0, y0))
                self.turns += 1
        elif y1 < y0:
            for i in range(abs(y0 - y1)):
                y0 -= 1
                self.moves.append((x0, y0))
                self.turns += 1
        else:
            pass

    def random_move(self, number: int = 1):
        """
        This method moves the Butterfly in a random direction the number of times specificed
        in the method call
        :param number: an integor, the number of times to move randomly
        :return: None | self
        """
        # Standard random move
        for i in range(number):
            # If it's on the border, check to see if it can exit
            if (self.can_exit or self.can_exit_north) and (self.position[0] in [self.area_length - 1, 0]
                                                               or self.position[1] in [self.area_width - 1, 0]):
                self.check_if_exit()
                if self.status == 'exit':
                    return
                else:
                    # This is the case where it can exit, but random chance prevented it from doing so, so it moves
                    # either north, west, east or south instead
                    self.turns += 1
                    self.decrement_food(self.food_unit)
                    x0 = x1 = self.position[0]
                    y0 = y1 = self.position[1]
                    if x0 - 1 >= 0:
                        x1 = x0 - 1
                    elif y0 - 1 >= 0:
                        y1 = y0 - 1
                    elif y0 + 1 <= self.area_width - 1:
                        y1 = y0 + 1
                    elif x0 + 1 <= self.area_length - 1:
                        x1 = x0 + 1
                    else:
                        raise ValueError("no idea where this butterfly is")
                    self.position = (x1, y1)
            # If it's on the border and can't exit, then this will make sure it makes some move
            elif self.position[0] in [self.area_length - 1, 0] or self.position[1] in [self.area_width - 1, 0]:
                self.turns += 1
                self.decrement_food(self.food_unit)
                x0 = x1 = self.position[0]
                y0 = y1 =self.position[1]
                if x0 - 1 >= 0:
                    x1 = x0 - 1
                elif y0 - 1 >= 0:
                    y1 = y0 - 1
                elif y0 + 1 <= self.area_width - 1:
                    y1 = y0 + 1
                elif x0 + 1 <= self.area_length - 1:
                    x1 = x0 + 1
                else:
                    raise ValueError("no idea where this butterfly is")
                self.position = (x1, y1)
            # Not on the border, so we use a random move generator
            else:
                coord = np.random.choice((0, 1))
                direction = np.random.choice((-1, 1))
                x0 = x1 = self.position[0]
                y0 = y1 = self.position[1]
                if coord == 0:
                    # Move north-south
                    if self.area_length - 1 > x0 > 0:
                        x1 = x0 + direction
                        self.decrement_food(self.food_unit)
                        self.moves.append((x1, y1))
                    else:
                        raise ValueError("Somehow it is on the border but didn't get "
                                         "the border check and tried to move.")
                else:
                    # Move east-west
                    if self.area_width - 1 > y0 > 0:
                        y1 = y0 + direction
                        self.decrement_food(self.food_unit)
                        self.moves.append((x1, y1))
                    else:
                        raise ValueError("Somehow it is on the border but didn't get "
                                         "the border check and tried to move.")

    def simple_move(self, direction: str = 'north'):
        """
        This method simply moves the monarch one unit in one direction. It's specific to the butterfly because
        it will try to leave if it is on the northernmost border. Other pollinator_types might not behave this way
        :param direction: A string giving the ordinal direction
        :return: simple returns the updated butterfly
        >>> b1 = Pollinator(position=(3,0))
        >>> b1.simple_move("worst")
        Traceback (most recent call last):
          File "C:\Program Files\JetBrains\PyCharm 2018.2.3\helpers\pycharm\docrunner.py", line 140, in __run
            compileflags, 1), test.globs)
          File "<doctest simple_move[2]>", line 1, in <module>
            b1.simple_move("worst")
          File "C:/Users/Joshua/PycharmProjects/pollinator_simulation/Butterflies.py", line 205, in simple_move
            assert (direction == 'north' or direction == 'south' or direction == 'east' or direction == 'west')
        AssertionError
        >>> b1.simple_move('north')
        >>> b1.food_level = 20
        >>> print(b1.position)
        (2, 0)
        >>> b1
        Pollinator: 20.0% food at (2, 0), status: alive
        >>> b1.moves.append(b1.position)
        >>> b1.moves
        [(3, 0), (2, 0)]
        """
        # Ensure a valid ordinal direction was passed into the function
        direction = direction.lower()
        assert (direction == 'north' or direction == 'south' or direction == 'east' or direction == 'west')
        # First check if it exits
        self.check_if_exit()
        if self.status == 'exit':
            return
        else:
            x0 = x1 = self.position[0]
            y0 = y1 = self.position[1]
            # if the pollinator is on the border, move randomly
            if x0 == 0 or x0 == self.area_length - 1 or \
                    y0 == 0 or y0 == self.area_width - 1:
                self.random_move()

            # Otherwise it will make a basic moves
            elif direction == 'north':
                x1 = x0 - 1
                self.moves.append((x1, y1))
                self.decrement_food(self.food_unit)

            elif direction == 'south':
                x1 = x0 + 1
                self.moves.append((x1, y1))
                self.decrement_food(self.food_unit)

            elif direction == 'east':
                y1 = y0 + 1
                self.moves.append((x1, y1))
                self.decrement_food(self.food_unit)

            elif direction == 'west':
                y1 = y0 - 1
                self.moves.append((x1, y1))
                self.decrement_food(self.food_unit)

            else:
                raise ValueError("Direction not recognized")

    def seek_resource(self, resource: str, incremental: bool=False) -> int:
        """
        The pollinator seeks the designated resource
        :param resource: A resource to seek must be declared
        :return: return sends it back when it is done, otherwise it modifies self and returns self and turns
        taken to complete the operation
        >>> b1 = Pollinator()
        >>> b1.food_level = 50
        >>> b1.seek_resource("food")
        >>> b1.position
        (3, 0)
        >>> b1.moves
        [(0, 0), (1, 0), (2, 0), (3, 0)]
        >>> b = Pollinator()
        >>> b.food_level = 50
        >>> b.seek_resource("shelter")
        >>> b.position
        (3, 0)
        >>> b.moves
        [(0, 0), (1, 0), (2, 0), (3, 0)]
        """
        # Let's make sure no zombie pollinator_types are looking for our resources
        if self.status == 'dead':
            return

        if incremental:
            times = 1
        else:
            times = np.random.randint(1, 11)
        if resource == 'shelter':
            if not self.shelter_indices:
                # There's no shelter, so it just wanders :(
                self.random_move(times)
                self.turns += times
                return
            else:
                if self.position in self.shelter_indices:
                    # In order to prevent a Butterfly from lingering on a food or shelter square
                    # too long, I'm introducing a 50-50 chance that it moves randomly if it's
                    # already on a square containing what it wants.
                    if np.random.choice([1, 0]):
                        nearest = self.position
                        # To ensure that at least one time unit is consumed if it doesn't move
                        self.turns += 1
                    else:
                        self.random_move(times)
                        self.turns += times
                        return
                else:
                    nearest = min(self.shelter_indices, key=lambda x: manhattan_distance(x, self.position))

        elif resource == 'food':
            if not self.food_indices:
                # There's no food, so it just wanders :(
                self.random_move(times)
                self.turns += times
                return
            else:
                if self.position in self.food_indices:
                    # Same as seeking shelter above
                    if np.random.choice([1, 0]):
                        nearest = self.position
                        self.turns += 1
                    else:
                        self.random_move(times)
                        self.turns += times
                        return
                else:
                    nearest = min(self.food_indices, key=lambda x: manhattan_distance(x, self.position))

        else:
            raise ValueError('Unknown resource')

        # Record the nearest value
        x = nearest[0]
        y = nearest[1]

        # There's a random chance it can't reach the resource, otherwise it does
        # and spends the appropriate amount of energy to get there

        if np.random.choice([1, 0], p=[0.999, 0.001]):
            self.record_moves(x, y)
            self.position = (x, y)
            self.decrement_food(self.turns * self.food_unit)
            return

        # Moves randomly instead of seeking resource. Better luck next time.
        else:
            self.random_move(times)
            self.food_level -= self.food_unit * times
            self.turns += times
            return

    def increment_time(self):
        """
        This takes seconds and hours and increments it according to a 24-hour clock. Although this theoretically
        shouldn't arise in this calculation, I want to account for if an unusually large number of seconds gets
        passed in, perhaps due to pollinator wandering, and increment the day as well as the time
        :param days: number of days elapsed
        :param hrs: integer number of hours, from 0-23.
        :param secs: arbitrary number of integer seconds. For every 3600 seconds, it will add an hour.
        :return: returns the new value for hours and seconds
        :return: self | none
        >>> f = Area([[1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 2, 2, 1]])
        >>> b1 = Pollinator(f)
        >>> b1.hours = 5
        >>> b1.seconds = 87273
        >>> b1.increment_time()
        >>> assert(b1.days == 1)
        >>> assert(b1.hours == 5)
        >>> assert(b1.seconds == 873)
        """

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
        Because pollinator_types all rely on flowers, they tend to be most active early and later in the day, preferring to
        shelter when the day is hottest, and all rest at night when the flowers are more or less dormant. This
        should allow me to generalize a day of a pollinator and get more specific in their pollinator_types. I'll assume a
        day runs from 4am to the next 4am, though a pollinator could jump into this method at any time. Those entering
        later will get a pro-rated day, though the assumption is the wrapper will run the sim until they die or leave,
        so not getting a full day for the first day shouldn't hurt them overall.
        :param hours: current number of seconds
        :param seconds: current hours
        :param days: number of days elapsed. This simulation section is desgined to cover one day and then quit, but
        of course that may not always happen. And a monarch may start on a different day rather than the first day
        of the simulation.
        :return: None | the Pollinator object, appropriately manipulated
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
                                        p=[self.shelter_chance, 1 - self.shelter_chance]):
                        self.sheltered = True

                # slightly less chance of taking shelter in a mixed food/shelter Land_Use
                elif self.area.array[self.position[0]][self.position[1]] == 4 and self.sheltered is False:
                    if np.random.choice([True, False], p=[.9 * self.shelter_chance,
                                                          1 - (.9 * self.shelter_chance)]):
                        self.sheltered = True

            # if it's near food, it will most likely try to eat
            # There's no class-level variable for this since all pollinator_types have to eat
            # and actively seek food sources in flowers.
            if self.area.array[self.position[0]][self.position[1]] == 2:
                if np.random.choice([True, False], p=[0.99, 0.01]):
                    self.food_level += 25

            # Less chance of eating in a mixed food/shelter Land_Use due to less food availability
            if self.area.array[self.position[0]][self.position[1]] == 4:
                if np.random.choice([True, False], p=[0.80, 0.2]):
                    self.food_level += 25

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
        """
        Very basic behavior for a generic pollinator
        :return: Self | None
        """
        self.seek_resource("food")

    def late_morning_activity(self):
        """
        Very basic behavior for a generic pollinator
        :return: Self | None
        """
        self.seek_resource("food")

    def afternoon_activity(self):
        """
        Very basic behavior for a generic pollinator
        :return: Self | None
        """
        self.seek_resource("food")

    def late_afternoon_activity(self):
        """
        Very basic behavior for a generic pollinator
        :return: Self | None
        """
        self.seek_resource('food')

    def night_time_activity(self):
        """
        Very basic behavior for a generic pollinator
        :return: Self | None
        """
        self.seek_resource('shelter')


