#!/home/joshua/anaconda3/bin/python

from Earth.Crust.Developed.farm import *
from Animal.Role import *
from Animal.Arthropod.Insect.Lepidoptera.Danaus.plexippus import *
import time
import pandas as pd
import copy


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


def basic_test(field: Area, iterations: int) -> None:
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