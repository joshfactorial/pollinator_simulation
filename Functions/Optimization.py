from Animal.Role import *
from Animal.Danaus.plexippus import *
from Land_Use.Developed.farm import *
import numpy as np
import pandas as pd
from Functions.Tests import *


def iterate_field(group: list = None, number_fields: int = 2) -> CropField:
    """
    Iterate groups of fields to find optimal arrangements. Group is a list of
    CropField objects, or we'll create some from the standard tests.
    :param group: The field group to be optimized
    :param number_fields: How many from the group to select.
    :return: Optimal cropfield
    >>>
    """
    if group:
        pass
    else:
        group = ['standard', 'food heavy', 'shelter heavy', "middle food windbreak",
                 'middle shelter windbreak', 'middle shelter windbreak 2', 'fallow']
    total = []
    for i in range(number_fields):
        temp = np.random.choice(group)
        if temp == 'standard':
            created = StandardTest(34)
        elif temp == 'food heavy':
            created = HeavyFoodTest(34)
        elif temp == 'shelter heavy':
            created = ShelterHeavyTest(34)
        elif temp == 'middle food windbreak':
            created = MiddleFoodWindbreakTest(34)
        elif temp == 'middle shelter windbreak':
            created = MiddleShelterWindbreakTest(34)
        elif temp == 'middle shelter windbreak 2':
            created = MiddleShelterWindbreakTest2(34)
        elif temp == 'fallow':
            created = FallowTest(34)
        else:
            created = temp
        total.append(created)
    return total


def optimize_field_group(number_of_fields: int=5, dead_goal: int = 25, exit_goal: int = 50,
                   num_iters: int = 1000, total_iters: int=100) -> tuple:
    '''
    The goal of this function is to find an optimal arrangement of fields. It will start with a single field and repeat
    it across several rows and columns, then run butterflies through the entire set and see if we can find an optimal
    arrangement of fields. For example, maybe a fallow field in the middle is best, or maybe if there are food borders
    around each field works best.
    :param number_of_fields:
    :param dead_goal:
    :param exit_goal:
    :param num_iters:
    :param total_iters:
    :return:
    '''
    master_list = []
    result_list = []
    exit_pct = 0
    dead_pct = 100
    iters = 0
    while exit_pct <= exit_goal and dead_pct >= dead_goal and iters <= total_iters:
        arrangement = iterate_field(number_fields=number_of_fields)
        master_field = arrangement[0]
        for i in range(1, len(arrangement)):
            master_field.concatenate(arrangement[i].array)
        # Simulate to see how well the field does
        for i in range(num_iters):
            b1 = Monarch(master_field)
            while b1.status == 'alive':
                b1.move_one_day()
            result_list.append(b1.status)
        dead_pct = result_list.count("dead")/len(result_list) * 100
        exit_pct = result_list.count("exit")/len(result_list) * 100
        master_list.append((iters, arrangement, dead_pct, exit_pct))
        if iters % 5 == 0:
            print("Working on iteration {}".format(iters))
        iters += 1
    dead_pct = []
    for item in master_list:
        dead_pct.append(item[2])
    min_index = dead_pct.index(min(dead_pct))
    return master_list[min_index]

