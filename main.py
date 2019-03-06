from Functions.Optimization import *
from Functions.run_tests import *

if __name__ == "__main__":
    """
    Main executable for the program
    You can choose to run each option. Add more options for more tests, such as bees or other pollinators
    """

    # This runs a Butterfly simulation on a fallow field. You can substitute in any pollinator. What the exact survival
    # rate should be, I don't know, though I figure for any random species, above 50% makes sense. If the rates are
    # much lower or higher, adjust the pollinator's death factor and exit chance until it seems to be right
    while True:
        answer = input("Test the parameters? (y/n): ")
        try:
            str(answer.lower()) in ('y', 'n')
        except ValueError:
            print("y or n only please")
            continue

        if answer.lower() == "y":
            field = FallowTest(34)
            results = []
            results_test = []
            results_test_2 = []
            results_test_3 = []
            for i in range(10):
                b1 = Monarch(field)
                while b1.status == 'alive':
                    b1.move_one_day()
                print(b1)
                results.append(b1.status)
                results_test.append((b1.days, b1.hours, b1.seconds))
                results_test_2.append(b1)
                results_test_3.append(b1.moves)
            print("Exit: {}".format(100 * results.count('exit')/len(results)))
            print("Dead: {}".format(100 * results.count('dead') / len(results)))
            print(results)
            print(results_test)
            break
        elif answer.lower() == 'n':
            break

    # This test takes a random collection of premade fields, arranges them randomly, then walks a pollinator through.
    # It does this a number of times then looks for the best ones. See the documentation of those functions to get an
    # idea how to adjust parameters. You can also create your own collection of fields to draw from.
    while True:
        answer = input("Try to find an optimal field of existing arrangements? (y/n): ")
        try:
            answer.lower() in ('y', 'n')
        except ValueError:
            print("y or n only please")

        if answer.lower() == 'n':
            break

        number = input("\tTotal number of fields to iterate: ")
        try:
            number = int(number)
            assert(number > 0)
        except ValueError:
            print("value must be an integer greater than zero: ")

        if answer.lower() == 'y':
            print(optimize_field_group(total_iters=25, number_of_fields=number))
            break

    # This test compares fields from the standard pool and sees which of the base fields is best. You can add more
    # fields in the farm.py module, or create a new module to model different types of developed land. I'll add more
    # in the future, such as urban or semi-urban area, although the CropField class could be used as an urban area
    # if you think of "crops" as "buildings and pavement" and arrange things as such.
    while True:
        answer = input("Run some standard tests? (y/n): ")
        try:
            answer.lower() in ('y', 'n')
        except ValueError:
            print('y or n only please')

        if answer.lower() == 'y':
            run_tests()
            break
        elif answer.lower() == 'n':
            break