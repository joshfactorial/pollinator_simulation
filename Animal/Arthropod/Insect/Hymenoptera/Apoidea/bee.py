#!/home/joshua/anaconda3/bin/python

from Animal.Role import *
from Earth.Crust.Developed.farm import *
import numpy as np


class Bee(Pollinator):
    """
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
    """

    food_unit = .225
    __death_factor = 0.01
    __can_exit = True
    __exit_chance = 0.1
    __shelter_chance = 0.5

    def __init__(self, area: CropField):
        Pollinator.__init__(self, area)
        self.sheltered = True
        # This gives the position of the nest. I'll assume the nest must be close to either food or shelter
        # One problem most bees have is destruction of their habitat means they won't make nests, so this seems
        # like a logical choice to me
        if area.shelter_indices:
            index = np.random.randint(len(area.shelter_indices))
            nest_position = area.shelter_indices[index]

        elif area.food_indices:
            index = np.random.randint(len(area.food_indices))
            nest_position = area.food_indices[index]

        # if there's no suitable nest building site, call an error
        else:
            raise ValueError("There is no suitable nesting site for bees. Ensure field has some food or shelter")

        # Initialize the bee's position to its nest.
        self.position = nest_position
        self.moves = [nest_position]
        self.nest_position = nest_position

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
