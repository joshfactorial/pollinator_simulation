#!/home/joshua/anaconda3/bin/python

from Animal.Role import Pollinator
import numpy as np
from Land_Use.Land import *


class Monarch(Pollinator):
    """
    This class creates the Monarch butterfly object. The monarch is modeled as migrating north. It's movement is
    mainly north, unless it is seeking food or shelter. It will seek shelter when night approaches and food when it is
    hungry, unless it is sheltered. It enters on the edge of the field in a random position. It also has an element of
    randomness to it's movement, as wind currents can blow the insect off course.
    >>> b1 = Monarch()
    >>> b1.food_level = 100
    >>> b1.position = [1,3]
    >>> print(b1.food_level)
    100
    >>> b1.position
    [1, 3]
    >>> b1
    Monarch: 100.0% food at [1, 3], status: alive
    >>> b2 = Monarch(days = 2, hours = 6, position = [1, 3])
    >>> b2.food_level = 100
    >>> print(b1)
    Monarch with 100.0% food at [1, 3], status: alive
    >>> b2.days
    2
    >>> b2.hours
    6
    """
    food_unit = 0.0225
    death_factor = 0.0000009
    can_exit_north = True
    exit_chance = 0.9
    shelter_chance = 0.01

    def __init__(self, area: Area = Area([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [4, 4, 4, 4]]),
                 days: int = 0, hours: int = 4, seconds: int = 0, position: list = [0, 0]):
        Pollinator.__init__(self, area, days, hours, seconds)
        # This gives the starting position, unless starting position was already declared
        if position == [0, 0]:
            __variable = np.random.choice([0, 1, 2, 3], p=[0.625, 0.125, 0.125, 0.125])
            if __variable == 0:
                temp_position = [self.area_length - 1, np.random.randint(self.area_width)]
            elif __variable == 1:
                temp_position = [np.random.randint(int(self.area_length/2), self.area_length-1), 0]
            elif __variable == 2:
                temp_position = [np.random.randint(int(self.area_length/2), self.area_length-1), self.area_width-1]
            else:
                if self.shelter_indices:
                    temp_position = list(self.shelter_indices[np.random.choice(len(self.shelter_indices))])
                else:
                    temp_position = [self.area_length - 1, 0]
            self.position = temp_position
            self.moves = [temp_position]
        else:
            self.position = position
            self.moves = [self.position[:]]
        if 4 <= self.hours < 6:
            self.sheltered = True

    def morning_activity(self):
        """
        For the first couple hours in the morning, monarchs will typically seek food.

        :return: None | self
        >>> b3 = Monarch(position=(1, 1))
        >>> b3.sheltered = False
        >>> b3.food_level = 50
        >>> b3
        Monarch: 50.0% food at (1, 1), status: alive
        >>> np.random.seed(0)
        >>> b3.morning_activity()
        >>> b3
        Monarch: 50.0% food at (3, 1), status: alive
        >>> b3.sheltered = True
        >>> b3.position = (0, 0)
        >>> b3.morning_activity()
        >>> assert(b3.sheltered is False)
        >>> b3.sheletere = True
        >>> b3.position = (3, 3)
        >>> b3.food_level = 10
        >>> assert(b3.sheltered is False)
        """
        # If it's in shelter during the day light, there's a small chance it will just stay put, unless
        # it is super hungry
        if self.sheltered:
            # number of times it will move randomly
            times = np.random.randint(10)
            # Just a check to make sure it is actually in a tree Land_Use and marked as sheltered...
            if self.area.array[self.position[0]][self.position[1]] not in [3, 4]:
                self.sheltered = False
                self.random_move(times)
                self.turns += times
            # if it's still sheltered but it's food level is low, or random chance kicks in, it will leave shelter
            elif self.food_level < 25 or np.random.choice([True, False], p=[0.1, 0.9]):
                self.sheltered = False
                self.random_move(times)
                self.seconds += times
            else:
                # just stay sheltered if those conditions fail
                # Consume half a unit of food
                self.decrement_food(self.food_unit / 2)
                self.turns += 1
        else:
            self.seek_resource('food')

    def late_morning_activity(self):
        """
        If it's daylight, the priorities will be food if it's hungry and moving north otherwise.
        It may randomly occasionally seek shelter if it happens to be near a tree.
        If it's in shelter during the day light, there's a small chance it will just stay put, unless
        it is super hungry
        :return: None | self
        >>> b3 = Monarch(position=(1, 1))
        >>> b3.sheltered = False
        >>> b3.food_level = 75
        >>> b3
        Monarch: 75.0% food at (1, 1), status: alive
        >>> np.random.seed(0)
        >>> b3.late_morning_activity()
        >>> b3
        Monarch: 59.6% food at (1, 1), status: alive
        >>> b3.sheltered = True
        >>> b3.position = (0, 0)
        >>> b3.morning_activity()
        >>> assert(b3.sheltered is False)
        >>> b3.sheletere = True
        >>> b3.position = (3, 3)
        >>> b3.food_level = 10
        >>> assert(b3.sheltered is False)
        """
        # moves possible
        moves_possible = int(self.food_level // self.food_unit)
        if self.sheltered:
            # number of times it moves randomly
            times = np.random.randint(10)
            # Just a check to make sure it is actually in a tree Land_Use and marked as sheltered...
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
                self.decrement_food(self.food_unit / 2)
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
        """
        Butterflies continue moving north into the afternoon
        :return: None | self
        """
        self.late_morning_activity()
        return

    def late_afternoon_activity(self):
        """
        As dusk approaches, it will try to look for food before sheltering for the night.
        :return: None | self
        >>> b4 = Monarch()
        >>> np.random.seed(0)
        >>> b4.sheltered = True
        >>> b4.late_afternoon_activity()
        >>> assert b4.sheltered == False
        >>> b4.position = (1, 1)
        >>> b4.food_level = 25
        >>> b4
        Monarch: 25.0% food at (1, 1), status: exit
        >>> b4.late_afternoon_activity()
        >>> b4
        Monarch: 24.8% food at (3, 1), status: exit
        """
        # Number of times to randomly move
        times = np.random.randint(10)
        # If it's still sheltered at this point, break shelter
        if self.sheltered:
            self.sheltered = False
            self.random_move(times)
            self.decrement_food(self.food_unit)
            self.turns += times
        else:
            # otherwise it's going to look for food to fill its belly before sleep, unless it's full
            if self.food_level <= 75 and self.food_indices:
                self.seek_resource('food')
            else:
                moves_possible = int(self.food_level // self.food_unit)
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
        return

    def night_time_activity(self):
        """
        During the evening, it will prioritize seeking shelter. It will stay in shelter through the night
        once it locates it, so we'll remove the leave shelter component of the checks. There's no real
        food to be had at night, so we'll just assume it battens down the hatches. If it's food falls too low
        it may die. Such is the risk of life.
        :return: None | self
        >>> b3 = Monarch()
        >>> b3.sheltered = True
        >>> b3.position = (0, 0)
        >>> b3.morning_activity()
        >>> assert(b3.sheltered is False)

        """


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
                self.decrement_food(self.food_unit / 2)
                return
        # This is the case that it is alive and near shelter. At this time it will take shelter
        elif self.area.array[self.position[0]][self.position[1]] in [3, 4]:
            self.sheltered = True
            self.decrement_food(self.food_unit / 2)

        else:
            # otherwise it's going to look for shelter
            if self.shelter_indices:
                self.seek_resource('shelter')
            else:
                for i in range(times):
                    self.simple_move("North")
                    self.turns += 1
        return

    def mating(self):
        """
        TODO: implement mating behavior
        The one rule of monarch mating is that they must lay their eggs on milkweed, defined as type 2 in the Area.
        :return: None | self
        """
        pass

    def laying_eggs(self):
        """
        TODO: implement egg laying
        :return: None | self
        """
        # Monarchs lay between 300 and 800 eggs, so I counted that as 2 standard deviations around a mean of 550, making
        # 90% of their behavior
        eggs_laid = np.random.normal(550, scale=125)
        # it tries to seek a place to lay it's food.
        # TODO: implement an incemental option for resource seeking to allow for a butterfly to abort the attempt and
        #  simply lay it's eggs wherever it is
        while self.food_level > 25:
            self.seek_resource('food', incremental=True)
            self.decrement_food(self.food_unit)
        location_of_eggs = self.position
        x = self.position[0]
        y = self.position[1]
        if location_of_eggs[x][y] == 2:
            #success
            pass
        else:
            #failure, the eggs all perish
            pass
        pass

    def caterpillar(self):
        """
        It takes 4-6 weeks to go from egg to butterfly. They can pupate as early as 4 weeks. So we'll pick
        an aribtrary time and that minus 1 will be when it pupates. I reckon it's chance for survival goes up if it
        gets that far. The total survival rate of a caterpillar is only about 10%. So, to calculate it's weekly survival
        rate, I assume each week's survival chance is uniform and independent, call it x. I then figure 10% is the lower
        bound, and that it will reach that if it stays a caterpillar the full 6 weeks. So x^6 <= 0.1 means it survives.
        So  x <= 0.61829 means that it survives each week. This implies, for example, that if it only goes 4 weeks,
        it has more like a 22% chance of survival, but it will have less food, thus reducing it's overall survival
        rate as an adult. So it's a tradeoff. Similar for the food it can eat.
        TODO: implement caterpillar survival
        :return: None | self
        """
        # We'll assume all caterpillars start with a basic amount of food supplied by the egg
        self.food_level == 25
        self.status == 'egg'
        random = np.random.randint(4, 7)
        for weeks in range(random + 1):
            chances = np.random.random()
            if weeks == random:
                self.status == 'pupa'
                if chances > 0.68219:
                    self.status == 'dead'
            elif weeks == 0:
                if chances > 0.68129:
                    self.status == 'dead'
                else:
                    self.status == 'caterpillar'
            else:
                if chances > 0.68129:
                    self.status = 'dead'
                else:
                    # So I figure if they go 5 weeks before pupating, they will have more food, and ultimately a butter
                    # chance for survival, but they run more risk of dying. One of those tradeoff things.
                    self.food_level += 18.75
            # If it died, discontinue the loop
            if self.status == 'dead':
                return
        if self.status == 'pupa':
            # If it survives the gauntlet, it is set to 'alive,' the default status for an adult butterfly! Yay!
            self.status == 'alive'