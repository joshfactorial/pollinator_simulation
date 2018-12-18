
#!/home/joshua/anaconda3/bin/python

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
            created = create_standard_test(34)
        elif temp == 'food heavy':
            created = create_food_heavy_test(34)
        elif temp == 'shelter heavy':
            created = create_shelter_heavy_test(34)
        elif temp == 'middle food windbreak':
            created = create_middle_food_windbreak_test(34)
        elif temp == 'middle shelter windbreak':
            created = create_middle_shelter_windbreak_test(34)
        elif temp == 'middle shelter windbreak 2':
            created = create_middle_shelter_windbreak_test_2(34)
        elif temp == 'fallow':
            created = create_fallow_test(34)
        else:
            created = temp
        total.append(created)
    return total


def optimize_field_group(field_group: list, dead_goal: int = 25, exit_goal: int = 50,
                   num_iters: int = 25, total_iters: int = math.inf) -> CropField:
    '''
    The goal of this function is to find an optimal arrangement of fields. It will start with a single field and repeat
    it across several rows and columns, then run butterflies through the entire set and see if we can find an optimal
    arrangement of fields. For example, maybe a fallow field in the middle is best, or maybe if there are food borders
    around each field works best.
    :param field:
    :param dead_goal:
    :param exit_goal:
    :param num_iters:
    :param total_iters:
    :return:
    '''
    master_list = []
    result_list = []
    exit = 0
    dead = 100
    iters = 0
    while exit <= exit_goal or dead >= dead_goal or iters <= num_iters:
        arrangement = iterate_field(field_group)
        master_field = arrangement[0]
        for i in range(1, len(arrangement)+1):
            master_field.concatenate(arrangement[i].array)
        # Simulate to see how well the field does
        for i in range(100):
            b1 = Monarch(master_field)
            while b1.status == 'alive':
                b1.move_one_day()
            result_list.append(b1.status)
        dead = result_list.count("dead")
        exit = result_list.count("exit")
        master_list.append((iters, master_field, dead, exit))
        iters += 1

