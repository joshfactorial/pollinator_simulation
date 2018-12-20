from Functions.Tests import *
from Functions.Visualizations import *


def run_tests():

    # first analysis
    master_results = {}
    for i in range(0, 5):
        test_field(master_results, i)
    index = ['standard', 'food_heavy', 'middle_food', 'middle_shelter', 'shelter_heavy']
    master_results = pd.DataFrame(master_results).T
    # print(master_results)
    master_results.index = index
    print("The best-performing field was {}".format(master_results[0].idxmin()))

    # field stats
    field = MiddleShelterWindbreakTest(34)
    food = np.count_nonzero(field.array == 2)
    shelter = np.count_nonzero(field.array == 3)
    crops = np.count_nonzero(field.array == 1)
    total = food + shelter + crops
    print('Percent food: {:.2f}%'.format(math.ceil(100 * food/total)))
    print("Percent shelter: {:.2f}%".format(math.ceil(100 * shelter/total)))
    print("Percent crops: {:.2f}%".format(math.floor(100 * crops/total)))

    # Testing a higher crop percentage variant of the middle row_len
    start_time = time.time()
    field_test = MiddleShelterWindbreakTest2(34)
    results = []
    for j in range(100):
        monarch1 = Monarch(field_test)
        monarch1.move_one_day()
        results.append(monarch1.status)
    print("Dead percentage = {:.2f}%".format(100 * results.count('dead') / len(results)))
    print("Exit percentage = {:.2f}%".format(100 * results.count('exit') / len(results)))
    print("--- %s seconds ---" % (time.time() - start_time))

    food = np.count_nonzero(field_test.array == 2)
    shelter = np.count_nonzero(field_test.array == 3)
    crops = np.count_nonzero(field_test.array == 1)
    total = food + shelter + crops
    print('Percent food: {:.2f}%'.format(math.ceil(100 * food/total)))
    print("Percent shelter: {:.2f}%".format(math.ceil(100 * shelter/total)))
    print("Percent crops: {:.2f}%".format(math.floor(100 * crops/total)))