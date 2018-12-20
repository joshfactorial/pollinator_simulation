from Land_Use.Developed.farm import *
from Animal.Danaus.plexippus import *
import time
import pandas as pd
import copy


def test_field(dictionary, number):
    # This function takes care of some repetitive code I had written earlier. It's not perfect, but it works for now.
    start_time = time.time()
    if number == 0:
        field_to_test = StandardTest(33)
    elif number == 1:
        field_to_test = HeavyFoodTest(33)
    elif number == 2:
        field_to_test = MiddleFoodWindbreakTest(33)
    elif number == 3:
        field_to_test = MiddleShelterWindbreakTest(33)
    elif number == 4:
        field_to_test = ShelterHeavyTest(33)
    else:
        return dictionary
    results = []
    for j in range(10):
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